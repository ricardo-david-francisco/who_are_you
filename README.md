# who_are_you

"Tell me what you like, I tell you who you are." This project builds a short
profile from your favourite music, film, art, architecture and books. A small
built‑in knowledge base links each item to descriptive tags. The program counts
those tags and summarises your dominant traits. A lightweight GPT‑Neo model can
also interpret the results in natural language.

## Quick start

Run the following command to install dependencies and launch the simple web
interface:

```bash
./start.sh
```

An ngrok URL will appear. Open it, pick around 5‑10 entries from each list and
read your generated profile.

If you prefer the command‑line version you can run:

```bash
python portrait.py             # interactive prompts
python portrait.py sample_profile.json  # use the example profile
```

## Google Colab demo

`colab_demo.ipynb` contains the same setup for Colab. Execute the cells to get
an ngrok link and interact with the form remotely.

## Local web page

`webapp.py` provides the minimal interface on your machine. It requires the same
packages as above and is invoked with `python webapp.py`. Feel free to adjust the
choices in `portrait.py` or add your own.

## Customising

All descriptive tags live in dictionaries at the top of `portrait.py`. Add,
remove or modify entries as you like – no database required. The program simply
counts the associated tags and builds a short summary, keeping the project
lightweight and easy to modify for non‑technical users.
