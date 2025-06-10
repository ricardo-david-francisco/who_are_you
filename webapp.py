import io
import os
from base64 import b64encode
from collections import Counter

from flask import Flask, request, render_template_string
from pyngrok import ngrok
from wordcloud import WordCloud
from transformers import pipeline

from portrait import ALL_DB, collect_tags, summarize

# HTML templates
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

# Initialize Flask app
app = Flask(__name__)

# Use EleutherAI/gpt-neo-125M for lightweight text generation
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Build user profile from form inputs
        profile = {cat: request.form.getlist(cat) for cat in ALL_DB}
        # Collect tags and summary
        tags = []
        for category, items in profile.items():
            tags.extend(collect_tags(category, items))
        summary = summarize(tags)
        # Generate GPT interpretation
        interpretation = generator(
            summary + "\nIn a short paragraph, describe this person:",
            max_length=100,
            num_return_sequences=1,
        )[0]["generated_text"]
        # Create word cloud image and encode as base64
        counter = Counter(tags)
        wc = WordCloud(width=800, height=400, background_color="white")
        wc.generate_from_frequencies(counter)
        img_io = io.BytesIO()
        wc.to_image().save(img_io, format="PNG")
        img_b64 = b64encode(img_io.getvalue()).decode("ascii")
        # Render result page
        return render_template_string(
            TEMPLATE_RESULT,
            summary=summary,
            wordcloud=img_b64,
            interpretation=interpretation,
        )

    # GET → show selection form
    return render_template_string(TEMPLATE_FORM, db=ALL_DB)

if __name__ == "__main__":
    # Expose via ngrok for public URL
    public_url = ngrok.connect(5000)
    print(" * ngrok tunnel:", public_url)
    app.run(port=5000)
