import io
import os
import getpass
from base64 import b64encode
from collections import Counter

from flask import Flask, request, render_template_string
from pyngrok import ngrok
from wordcloud import WordCloud
from transformers import pipeline

from portrait import ALL_DB, collect_tags, summarize

# ─── Prompt for ngrok auth token ────────────────────────────────────────────────
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
if not NGROK_AUTH_TOKEN:
    NGROK_AUTH_TOKEN = getpass.getpass("Enter your ngrok auth token: ")
# register and then immediately delete for security
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
del NGROK_AUTH_TOKEN
# ────────────────────────────────────────────────────────────────────────────────

# ─── Inline CSS for dark, centered, modern theme ────────────────────────────────
BASE_CSS = """
<style>
  body {
    background-color: #121212;
    color: #E0E0E0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0;
    padding: 0;
    min-height: 100vh;
  }
  .container {
    width: 90%;
    max-width: 700px;
    text-align: center;
    padding: 20px;
  }
  h1.banner {
    background-color: #1F1B24;
    color: #BB86FC;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
    font-size: 1.6em;
  }
  h2 {
    margin-top: 1.5em;
    color: #BB86FC;
  }
  select, input[type=submit] {
    background-color: #1F1B24;
    color: #E0E0E0;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 8px;
    font-size: 1em;
    margin-top: 8px;
  }
  select {
    width: 100%;
  }
  input[type=submit] {
    cursor: pointer;
    background-color: #BB86FC;
    color: #121212;
    border: none;
    font-weight: bold;
    margin-top: 20px;
  }
  img.wordcloud {
    max-width: 100%;
    border-radius: 8px;
    margin: 20px 0;
  }
  pre {
    background-color: #1F1B24;
    padding: 15px;
    border-radius: 8px;
    text-align: left;
    overflow-x: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
  a {
    color: #BB86FC;
    text-decoration: none;
    font-weight: bold;
  }
  a:hover {
    text-decoration: underline;
  }
</style>
"""

TEMPLATE_FORM = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Emotional Portrait</title>
  {BASE_CSS}
</head>
<body>
  <div class="container">
    <h1 class="banner">Tell me what you like, I'll tell you who you are</h1>
    <h2>Select 5–10 items from each category</h2>
    <form method="post">
      {{% for category, items in db.items() %}}
        <h3>{{{{ category.title() }}}}</h3>
        <select name="{{{{ category }}}}" multiple size="8" required>
          {{% for item in items.keys() %}}
            <option value="{{{{ item }}}}">{{{{ item }}}}</option>
          {{% endfor %}}
        </select>
      {{% endfor %}}
      <br>
      <input type="submit" value="Generate Portrait">
    </form>
  </div>
</body>
</html>
"""

TEMPLATE_RESULT = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Your Emotional Portrait</title>
  {BASE_CSS}
</head>
<body>
  <div class="container">
    <h1 class="banner">Tell me what you like, I'll tell you who you are</h1>
    <h2>Your Emotional Portrait</h2>
    <p>{{{{ summary }}}}</p>
    <img class="wordcloud" src="data:image/png;base64,{{{{ wordcloud }}}}" alt="Word Cloud">
    <h2>GPT Interpretation & Daily Life</h2>
    <pre>{{{{ interpretation }}}}</pre>
    <a href="/">Try again</a>
  </div>
</body>
</html>
"""

app = Flask(__name__)

# More creative generation settings
generator = pipeline(
    "text-generation",
    model="EleutherAI/gpt-neo-125M",
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Build profile & collect tags
        profile = {cat: request.form.getlist(cat) for cat in ALL_DB}
        tags = []
        for cat, items in profile.items():
            tags.extend(collect_tags(cat, items))
        summary = summarize(tags)

        # Enhanced prompt
        prompt = (
            "You are an insightful personality profiler. "
            "Given this summary of someone's tastes, produce:\n"
            "1) A deep personality analysis\n"
            "2) A guess at who they might be\n"
            "3) A description of their typical daily life\n\n"
            f"{summary}\n\n"
            "Personality & Daily Life Profile:"
        )
        interpretation = generator(
            prompt,
            max_length=200,
            num_return_sequences=1,
        )[0]["generated_text"].strip()

        # Word cloud image
        counter = Counter(tags)
        wc = WordCloud(width=800, height=400, background_color="white")
        wc.generate_from_frequencies(counter)
        img_io = io.BytesIO()
        wc.to_image().save(img_io, format="PNG")
        img_b64 = b64encode(img_io.getvalue()).decode("ascii")

        return render_template_string(
            TEMPLATE_RESULT,
            summary=summary,
            wordcloud=img_b64,
            interpretation=interpretation,
        )

    return render_template_string(TEMPLATE_FORM, db=ALL_DB)

if __name__ == "__main__":
    public_url = ngrok.connect(5000)
    print(" * ngrok tunnel:", public_url)
    app.run(port=5000)
