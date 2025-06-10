# who_are_you

"Tell me what you like, I tell you who you are." This project builds an emotional profile from your favourite music, movies, painters, architecture and books. Each item is mapped to descriptive tags in a small built‑in database. The tags are tallied to reveal dominant traits, and a lightweight GPT‑Neo model can interpret the results in plain language.

## Quick start

Use the helper script to install everything and launch the demo web page:

```bash
./start.sh
```

When the script finishes a public URL will appear in the terminal. Open it, pick 5‑10 entries from each list and you will see a word cloud alongside a short GPT‑generated portrait.

If you prefer the command line you can run the script directly:

```bash
python portrait.py             # prompts interactively
python portrait.py sample_profile.json  # analyse the example file
```

## Google Colab

`colab_demo.ipynb` shows how to run everything in Colab. Because notebooks loaded directly from GitHub do not include the rest of the repository, the first cell clones the repo and moves into it:

```python
!git clone https://github.com/<your-username>/who_are_you.git
%cd who_are_you
```

After that run the remaining cells. They install the dependencies and start the server. Gradio will print a public link which you can open to select your favourites and view the generated portrait.

## Local web page

`webapp.py` starts a small Gradio interface with multi‑select lists. It generates the same summary, word cloud and GPT interpretation as the command‑line version. Invoke it with `python webapp.py` if you already installed the requirements. Gradio will display a link you can share.

## Customising

All tags live in dictionaries near the top of `portrait.py`. Add or remove entries as you like – no database is required. The program simply counts the associated tags and summarises them, keeping the project lightweight and easy to modify for non‑technical users.
