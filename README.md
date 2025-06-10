# who_are_you

This repository contains a small Python tool for generating an "emotional portrait" from a set of your favorite artists and works. Provide a JSON file listing your preferred music artists, movies, painters, pieces of architecture and books, and the script will analyse them using a simple knowledge base of descriptive tags.

```
python portrait.py sample_profile.json
```

`sample_profile.json` shows the expected structure. Each key corresponds to a category and the values are lists of your favorites. The sample file contains a few example artists, movies, painters, buildings and books.

## Google Colab demo

The repository includes `colab_demo.ipynb` which launches a small Flask web application using ngrok. Open the notebook in [Google Colab](https://colab.research.google.com/) and run the cells. A public ngrok URL will be printed where you can pick between five and ten items from each category. The app will generate a word cloud and, using a small GPT‑2 model, produce a short interpretation of your profile.

## Local web page

`webapp.py` implements the web server used by the Colab notebook. You can also run it locally if you have `flask`, `pyngrok`, `wordcloud` and `transformers` installed.

```
python webapp.py
```
