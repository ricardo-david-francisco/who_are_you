# who_are_you

"Tell me what you like, I tell you who you are" – this project builds a short profile based on your taste in music, film, art, architecture and literature.  A small built‑in knowledge base links each artist or work to three or more descriptive tags.  By providing your favourites, the program collects those tags and summarises the traits they share.  The same information powers a tiny web app that displays a word cloud and uses a lightweight GPT‑Neo model to guess at deeper aspects of your personality.

Run the script and follow the prompts. For each category you'll see a numbered list of options; type the numbers of your favourites (5‑10 works best). You can still pass a JSON file if you prefer:

```
python portrait.py my_profile.json  # optional
```

The sample file shows the expected structure if you want to prepare one manually, but most users can simply run the program and pick from the lists. The output lists the most common descriptive tags and a short textual summary.

## Google Colab demo

`colab_demo.ipynb` installs the few dependencies and then runs `webapp.py` for you.  After executing the notebook in [Google Colab](https://colab.research.google.com/), an ngrok URL appears.  Open it and you'll see simple multi‑select boxes for every category.  Choose your favourites (hold **Ctrl** or **Cmd** to select multiple) and submit the form.  The server returns a word cloud of your dominant traits together with a GPT‑Neo generated interpretation of what those choices might reveal about you.

## Local web page

`webapp.py` contains the same minimal interface as the Colab notebook but runs on your machine.  Install `flask`, `pyngrok`, `wordcloud` and `transformers`, then start the server with:

```bash
python webapp.py
```
It prints an ngrok link you can open in your browser.  The page lets you pick your favourite items, view the resulting word cloud and read the personality summary.  Everything is plain HTML for easy maintenance – feel free to adjust the choices in `portrait.py` or add your own.

## Customising

All the descriptive tags live in dictionaries at the top of `portrait.py`.  Add, remove or change entries as you like – no database required.  The program simply counts the associated tags and builds a summary from the most common ones.  Keeping the data in code makes the project lightweight and easy to modify for non‑technical users.
