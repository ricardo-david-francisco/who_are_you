# who_are_you

"Tell me what you like, I tell you who you are." This tool builds a personal profile from your favourite music, movies, painters, architecture and books. Each item has descriptive tags in a small built‑in database. The tags are tallied to reveal dominant traits and a lightweight GPT‑Neo model interprets the results in plain language.

## Quick start

Run the helper script to install requirements and launch the web interface. It
opens a small dark themed page in Gradio:

```bash
./start.sh
```

A shareable URL will appear. Open it and choose five to ten items from each list to see a word cloud and GPT‑generated portrait. On the command line you can also run:

```bash
python portrait.py             # prompts interactively
python portrait.py sample_profile.json  # analyse the example file
```

## Google Colab

`colab_demo.ipynb` shows how to use the project in Colab. If the notebook cannot find `webapp.py`, clone the repository first and change into it:

```python
!git clone https://github.com/<your-username>/who_are_you.git
%cd who_are_you
```

Then run the remaining cells to install dependencies and launch Gradio. A public
link will appear so you can select your favourites and view the portrait. The
notebook uses `start.sh` which installs packages quietly and launches the app in
one step.

## Local web page

`webapp.py` starts a small Gradio form with multi‑select lists. Launch it with `python webapp.py` (or via the Docker image below) and share the link Gradio prints.

## Docker

A simple Dockerfile is provided. Build and run it like so:

```bash
docker build -t who_are_you:1.0 .
docker run -p 7860:7860 who_are_you:1.0
```

The container automatically launches the web app.

## Backup

Run `backup.sh` to create a `who_are_you_backup.tar.gz` archive containing all project files.

## Version 1.0

This is the initial release. It includes the interactive command line tool, a Gradio web interface, and example data. Everything was assembled in roughly an hour and a half.

## Future ideas

* Attach images for buildings, paintings, book covers and movie posters
* Expand the architecture list with more landmarks
* Pull best‑seller book information and movie metadata from TMDB
* Upgrade the language model for deeper analysis

## Customising

All tags live in dictionaries at the top of `portrait.py`. Add or remove entries as you like—no database is required. The simple design makes it easy to maintain for non‑technical users.
