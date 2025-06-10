from collections import Counter

import gradio as gr
from wordcloud import WordCloud
from transformers import pipeline

from portrait import ALL_DB, collect_tags, summarize

# Use a lightweight open-source model that provides higher quality than GPT-2
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

def generate_portrait(music, movies, painters, architecture, books):
    profile = {
        "music": music or [],
        "movies": movies or [],
        "painters": painters or [],
        "architecture": architecture or [],
        "books": books or [],
    }
    tags = []
    for c, items in profile.items():
        tags.extend(collect_tags(c, items))
    summary = summarize(tags)
    counter = Counter(tags)
    wc = WordCloud(width=800, height=400, background_color="white")
    wc.generate_from_frequencies(counter)
    img = wc.to_image()
    interpretation = generator(
        summary + "\nIn a short paragraph, describe this person:",
        max_length=100,
        num_return_sequences=1,
    )[0]["generated_text"]
    return summary, img, interpretation

CSS = """
body{background-color:#111;color:#eee;text-align:center;}
.gradio-container{margin:0 auto;}
"""

with gr.Blocks(theme=gr.themes.Soft(), css=CSS) as demo:
    gr.Markdown("# Tell me what you like...I'll tell you who you really are!")
    gr.Markdown("## Emotional Portrait")
    with gr.Row():
        music = gr.Dropdown(list(ALL_DB["music"].keys()), multiselect=True, label="Music")
        movies = gr.Dropdown(list(ALL_DB["movies"].keys()), multiselect=True, label="Movies")
    with gr.Row():
        painters = gr.Dropdown(list(ALL_DB["painters"].keys()), multiselect=True, label="Painters")
        architecture = gr.Dropdown(list(ALL_DB["architecture"].keys()), multiselect=True, label="Architecture")
    books = gr.Dropdown(list(ALL_DB["books"].keys()), multiselect=True, label="Books")
    generate_btn = gr.Button("Generate")
    summary_out = gr.Textbox(label="Summary")
    cloud_out = gr.Image(label="Word Cloud")
    interp_out = gr.Textbox(label="GPT Interpretation")

    generate_btn.click(
        generate_portrait,
        inputs=[music, movies, painters, architecture, books],
        outputs=[summary_out, cloud_out, interp_out],
    )

if __name__ == "__main__":
    demo.launch(share=True)