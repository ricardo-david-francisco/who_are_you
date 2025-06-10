import os
import json
from collections import Counter
from base64 import b64encode

from flask import Flask, request, render_template_string
from pyngrok import ngrok
from wordcloud import WordCloud
from transformers import pipeline

from portrait import ALL_DB, collect_tags, summarize

TEMPLATE_FORM = """
<!doctype html>
<title>Emotional Portrait</title>
<h1>Select 5-10 items from each category</h1>
<form method="post">
{% for category, items in db.items() %}
<h2>{{ category.title() }}</h2>
<select name="{{ category }}" multiple size="10" required>
{% for item in items.keys() %}
  <option value="{{ item }}">{{ item }}</option>
{% endfor %}
</select>
{% endfor %}
<br><input type="submit" value="Generate">
</form>
"""

TEMPLATE_RESULT = """
<!doctype html>
<title>Result</title>
<h1>Your Emotional Portrait</h1>
<p>{{ summary }}</p>
<img src="data:image/png;base64,{{ wordcloud }}" alt="Word Cloud">
<h2>GPT Interpretation</h2>
<pre>{{ interpretation }}</pre>
<a href="/">Try again</a>
"""

app = Flask(__name__)

# Use a lightweight open-source model that provides higher quality than GPT-2
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        profile = {}
        for category in ALL_DB:
            profile[category] = request.form.getlist(category)
        tags = []
        for c, items in profile.items():
            tags.extend(collect_tags(c, items))
        summary = summarize(tags)
        interpretation = generator(summary + "\nIn a short paragraph, describe this person:",
                                   max_length=100, num_return_sequences=1)[0]["generated_text"]
        counter = Counter(tags)
        wc = WordCloud(width=800, height=400, background_color="white")
        wc.generate_from_frequencies(counter)
        img_path = "wordcloud.png"
        wc.to_file(img_path)
        with open(img_path, "rb") as f:
            encoded = b64encode(f.read()).decode("ascii")
        os.remove(img_path)
        return render_template_string(TEMPLATE_RESULT, summary=summary,
                                      wordcloud=encoded,
                                      interpretation=interpretation)
    return render_template_string(TEMPLATE_FORM, db=ALL_DB)

if __name__ == "__main__":
    public_url = ngrok.connect(5000)
    print(" * ngrok tunnel: ", public_url)
    app.run()
