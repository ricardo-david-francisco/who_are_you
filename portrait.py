import json
from collections import Counter
from textwrap import fill

# Simplified knowledge base mapping items to descriptive tags
MUSIC_TAGS = {
    "Beethoven": ["dramatic", "revolutionary", "emotional depth"],
    "Mozart": ["brilliant", "classical elegance", "melodic clarity"],
    "Bach": ["complex", "structured", "harmonic mastery"],
    "Tchaikovsky": ["romantic", "melodic", "orchestral color"],
    "Rachmaninoff": ["expressive", "virtuosic", "rich harmony"],
    "Ennio Morricone": ["innovative", "atmospheric", "emotional"],
    "Hans Zimmer": ["modern", "textural", "intense"],
    "John Williams": ["melodic", "grand", "nostalgic"],
    "John Coltrane": ["spiritual", "improvisational", "exploratory"],
    "Miles Davis": ["cool", "innovative jazz", "moody"],
    "The Beatles": ["innovative", "melodic songwriting", "cultural impact"],
    "Pink Floyd": ["psychedelic", "conceptual", "atmospheric"],
    "Radiohead": ["introspective", "innovative", "melancholic"],
    "Bob Marley": ["uplifting", "spiritual", "social conscience"],
    "Nina Simone": ["soulful", "intense", "resilient"],
    "Massive Attack": ["dark", "atmospheric", "moody"],
    "Aphex Twin": ["experimental", "electronic", "textural"],
    "Explosions in the Sky": ["post-rock", "cinematic", "epic"],
    "Ludovico Einaudi": ["minimalist", "evocative", "contemporary"],
    "Arvo Pärt": ["spiritual", "minimalism", "meditative"],
    "Queen": ["anthemic", "theatrical", "diverse"],
    "David Bowie": ["chameleonic", "art rock", "influential"],
    "Prince": ["funky", "genre-blending", "iconic"],
    "Led Zeppelin": ["hard rock", "mythic", "bluesy"],
    "Jimi Hendrix": ["innovative", "guitar-driven", "psychedelic"],
    "The Rolling Stones": ["gritty", "rock & roll", "enduring"],
    "Beyoncé": ["empowering", "dynamic", "genre-defying"],
    "Taylor Swift": ["storytelling", "pop", "relatable"],
    "Billie Eilish": ["dark pop", "whispery", "youthful"],
    "Adele": ["soulful", "powerful vocals", "emotional"],
    "Kanye West": ["boundary-pushing", "influential", "innovative"],
    "Kendrick Lamar": ["lyrical", "conscious", "poetic"],
    "Drake": ["melodic rap", "catchy", "mainstream"],
    "Daft Punk": ["electronic", "retro-futuristic", "innovative"],
    "The Weeknd": ["dark", "synth-heavy", "moody"],
    "Lana Del Rey": ["cinematic", "nostalgic", "melancholic"],
    "Sia": ["anthemic", "soaring vocals", "emotional"],
    "Florence + The Machine": ["epic", "art pop", "powerful"],
    "St. Vincent": ["experimental", "guitar-driven", "art rock"],
    "Frank Ocean": ["emotional", "genre-blurring", "innovative"],
    "Childish Gambino": ["multifaceted", "creative", "genre-fluid"],
    "Rihanna": ["versatile", "catchy", "pop icon"],
    "Shakira": ["rhythmic", "global", "dynamic"],
    "Shostakovich": ["tense", "ironic", "innovative"],
    "Mahler": ["expansive", "spiritual", "emotional"],
    "Debussy": ["impressionistic", "atmospheric", "colorful"],
    "Chopin": ["lyrical", "virtuosic", "romantic"],
    "Vivaldi": ["baroque", "energetic", "seasonal"],
    "Ella Fitzgerald": ["jazzy", "scat", "timeless"],
    "Louis Armstrong": ["charismatic", "jazzy", "iconic"],
    "Duke Ellington": ["swing", "orchestral jazz", "innovative"],
    "Skrillex": ["dubstep", "energetic", "experimental"],
    "Avicii": ["uplifting", "EDM", "melodic"],
    "The Doors": ["poetic", "psychedelic rock", "emotional intensity"],
    "Paco de Lucía": ["flamenco", "virtuosic", "passionate"],
}

MOVIE_TAGS = {
    "The Godfather": ["epic", "crime", "family dynamics"],
    "Citizen Kane": ["innovative", "cinematic milestone", "complex narrative"],
    "Pulp Fiction": ["stylized", "nonlinear", "edgy"],
    "Blade Runner": ["atmospheric", "visionary", "noir"],
    "2001: A Space Odyssey": ["austere", "philosophical", "innovative"],
    "Casablanca": ["romantic", "timeless", "dramatic tension"],
    "Shawshank Redemption": ["hopeful", "friendship", "dramatic storytelling"],
    "Inception": ["mind-bending", "dreamlike", "complex"],
    "Spirited Away": ["imaginative", "whimsical", "emotional"],
    "Parasite": ["social critique", "thriller", "satirical"],
    "The Matrix": ["revolutionary", "cyberpunk", "philosophical"],
    "Forrest Gump": ["heartwarming", "nostalgic", "epic journey"],
    "Schindler’s List": ["historical", "powerful", "tragic"],
    "Jurassic Park": ["adventurous", "groundbreaking", "thrilling"],
    "Titanic": ["romantic", "disaster", "epic"],
    "Star Wars": ["mythic", "sci-fi", "adventurous"],
    "The Lord of the Rings": ["fantasy", "epic", "heroic"],
    "Fight Club": ["dark", "subversive", "psychological"],
    "Goodfellas": ["crime", "gritty", "realistic"],
    "The Dark Knight": ["superhero", "intense", "philosophical"],
    "Amélie": ["whimsical", "romantic", "quirky"],
    "La La Land": ["musical", "romantic", "dreamy"],
    "The Silence of the Lambs": ["thriller", "psychological", "chilling"],
    "Pan’s Labyrinth": ["fantasy", "dark", "poetic"],
    "Avatar": ["visual spectacle", "sci-fi", "environmental"],
    "Gladiator": ["epic", "historical", "revenge"],
    "Saving Private Ryan": ["war", "intense", "heroic"],
    "Interstellar": ["sci-fi", "emotional", "cosmic"],
    "The Grand Budapest Hotel": ["quirky", "colorful", "stylized"],
    "Her": ["futuristic", "romantic", "introspective"],
    "Oldboy": ["violent", "revenge", "twist"],
    "No Country for Old Men": ["tense", "neo-western", "philosophical"],
    "Joker": ["dark", "psychological", "character-driven"],
    "Whiplash": ["intense", "musical", "ambitious"],
    "The Social Network": ["biographical", "driven", "cultural impact"],
    "The Revenant": ["harsh", "survival", "visceral"],
    "Moonlight": ["intimate", "poetic", "coming-of-age"],
    "The Big Lebowski": ["comedy", "cult", "quirky"],
    "Blade Runner 2049": ["visual", "philosophical", "neo-noir"],
    "Crouching Tiger, Hidden Dragon": ["martial arts", "mythic", "romantic"],
    "City of God": ["gritty", "urban", "realistic"],
    "The Shining": ["horror", "psychological", "iconic"],
    "Rear Window": ["suspenseful", "classic", "tense"],
    "Vertigo": ["psychological", "obsessive", "stylish"],
    "Lost in Translation": ["introspective", "romantic", "atmospheric"],
    "12 Angry Men": ["dialogue-driven", "tension", "moral conflict"],
    "WALL-E": ["animated", "charming", "environmental"],
    "Up": ["emotional", "adventurous", "heartwarming"],
    "Inside Out": ["imaginative", "emotional", "animated"],
}

PAINTER_TAGS = {
    "Leonardo da Vinci": ["innovative", "detailed", "scientific approach"],
    "Michelangelo": ["grand", "spiritual", "detailed sculptural sense"],
    "Picasso": ["abstract", "bold", "innovative"],
    "Van Gogh": ["emotive", "vibrant", "turbulent"],
    "Rembrandt": ["dramatic", "introspective", "light mastery"],
    "Monet": ["impressionistic", "light-focused", "nature-inspired"],
    "Dali": ["surreal", "dreamlike", "bizarre"],
    "Klimt": ["ornate", "symbolic", "decorative"],
    "Jackson Pollock": ["abstract", "energetic", "expressive"],
    "Frida Kahlo": ["personal", "symbolic", "colorful"],
    "Georges Seurat": ["pointillism", "detailed", "innovative"],
    "Henri Matisse": ["colorful", "bold", "fauvism"],
    "Georgia O’Keeffe": ["botanical", "vivid", "abstract"],
    "Edvard Munch": ["emotional", "expressionist", "moody"],
    "Edward Hopper": ["lonely", "realist", "urban"],
    "Caravaggio": ["dramatic", "chiaroscuro", "intense"],
    "Jean-Michel Basquiat": ["graffiti", "raw", "expressive"],
    "Andy Warhol": ["pop art", "commercial", "iconic"],
    "Claude Lorrain": ["landscape", "luminous", "classical"],
    "Grant Wood": ["regionalist", "American", "realist"],
    "Diego Rivera": ["muralist", "social", "historical"],
    "Joan Miró": ["playful", "surreal", "symbolic"],
    "Wassily Kandinsky": ["abstract", "spiritual", "colorful"],
    "Paul Cézanne": ["post-impressionist", "structured", "geometric"],
    "Marc Chagall": ["dreamlike", "fantastical", "colorful"],
    "Rene Magritte": ["surreal", "enigmatic", "conceptual"],
    "J.M.W. Turner": ["dramatic", "atmospheric", "luminous"],
    "Piet Mondrian": ["geometric", "primary colors", "abstract"],
    "Egon Schiele": ["expressive", "distorted", "figurative"],
    "Hieronymus Bosch": ["fantastical", "detailed", "symbolic"],
    "Francisco Goya": ["dark", "political", "dramatic"],
    "Mary Cassatt": ["impressionist", "intimate", "domestic"],
    "Jan Vermeer": ["detailed", "light", "genre scenes"],
    "Albrecht Dürer": ["detailed", "Renaissance", "technical"],
    "Jean-Auguste-Dominique Ingres": ["classical", "elegant", "portraiture"],
    "John Singer Sargent": ["portrait", "fluid", "luminous"],
    "Edgar Degas": ["movement", "ballet", "impressionist"],
    "Salvador Dalí": ["surreal", "dreamlike", "eccentric"],
    "David Hockney": ["modern", "colorful", "pop art"],
    "Yayoi Kusama": ["avant-garde", "polka dots", "installations"],
    "Banksy": ["street art", "political", "mysterious"],
    "Keith Haring": ["bold", "graffiti", "iconic"],
    "Takashi Murakami": ["pop", "Japanese", "colorful"],
    "Gustave Courbet": ["realist", "earthy", "provocative"],
    "Élisabeth Vigée Le Brun": ["portraiture", "elegant", "18th-century"],
    "Artemisia Gentileschi": ["baroque", "powerful", "feminist"],
    "Norman Rockwell": ["American", "narrative", "nostalgic"],
    "Paul Gauguin": ["vivid", "tropical", "symbolist"],
    "Lucian Freud": ["realist", "psychological", "intense"],
}

ARCHITECTURE_TAGS = {
    "Parthenon": ["classical", "balanced", "enduring"],
    "Colosseum": ["ancient", "monumental", "historic"],
    "Notre-Dame Cathedral": ["gothic", "detailed", "spiritual"],
    "Taj Mahal": ["elegant", "romantic", "grand"],
    "Sagrada Familia": ["organic", "ornate", "imaginative"],
    "Fallingwater": ["integrated", "modern", "natural"],
    "Eiffel Tower": ["iconic", "ironwork", "landmark"],
    "Sydney Opera House": ["iconic", "innovative", "sculptural"],
    "Guggenheim Bilbao": ["contemporary", "sculptural", "innovative"],
    "Burj Khalifa": ["tallest", "modern", "ambitious"],
    "Pantheon": ["ancient", "dome", "engineering"],
    "Petra": ["ancient", "carved", "rock-cut"],
    "Angkor Wat": ["grand", "spiritual", "historic"],
    "Neuschwanstein Castle": ["romantic", "fairytale", "picturesque"],
    "St. Basil’s Cathedral": ["colorful", "iconic", "Russian"],
    "Empire State Building": ["art deco", "skyscraper", "iconic"],
    "Chrysler Building": ["art deco", "ornate", "New York"],
    "Villa Savoye": ["modernist", "Le Corbusier", "functional"],
    "Louvre Pyramid": ["modern", "glass", "juxtaposed"],
    "Buckingham Palace": ["regal", "historic", "British"],
    "Hagia Sophia": ["byzantine", "historic", "monumental"],
    "Brandenburg Gate": ["neoclassical", "symbolic", "Berlin"],
    "Golden Gate Bridge": ["engineering", "iconic", "landmark"],
    "Shwedagon Pagoda": ["spiritual", "gilded", "Myanmar"],
    "CN Tower": ["tallest", "observation", "Canadian"],
    "The Shard": ["contemporary", "glass", "London"],
    "Petronas Towers": ["twin", "modern", "Malaysia"],
    "Gherkin": ["modern", "iconic", "London"],
    "Dome of the Rock": ["religious", "ornate", "historic"],
    "Space Needle": ["futuristic", "Seattle", "observation"],
    "Stonehenge": ["mysterious", "prehistoric", "monumental"],
    "Solomon R. Guggenheim Museum": ["Frank Lloyd Wright", "spiral", "modern"],
    "Alhambra": ["Islamic", "palatial", "decorative"],
    "Palace of Versailles": ["baroque", "grand", "historic"],
    "Flatiron Building": ["triangular", "New York", "iconic"],
    "Lotus Temple": ["modern", "flower-shaped", "spiritual"],
    "Marina Bay Sands": ["modern", "luxurious", "Singapore"],
    "La Pedrera (Casa Milà)": ["Gaudi", "organic", "undulating"],
    "The High Line": ["urban", "park", "adaptive reuse"],
    "Capitol Building": ["neoclassical", "dome", "government"],
    "UN Headquarters": ["international", "modernist", "symbolic"],
    "Cologne Cathedral": ["gothic", "twin spires", "German"],
    "Duomo di Milano": ["gothic", "elaborate", "Italian"],
    "Potala Palace": ["Tibetan", "palatial", "historic"],
    "Catherine Palace": ["rococo", "ornate", "Russian"],
    "Mont-Saint-Michel": ["island", "medieval", "picturesque"],
    "Burj Al Arab": ["luxurious", "iconic", "Dubai"],
    "Sydney Harbour Bridge": ["engineering", "iconic", "Australian"],
    "Museum of Tomorrow": ["futuristic", "innovative", "Brazil"],
}

BOOK_TAGS = {
    "Pride and Prejudice": ["romantic", "social commentary", "witty"],
    "To Kill a Mockingbird": ["compassionate", "social justice", "coming-of-age"],
    "1984": ["dystopian", "thought-provoking", "political"],
    "The Lord of the Rings": ["epic", "heroic", "mythic"],
    "Moby Dick": ["obsessive", "symbolic", "adventurous"],
    "War and Peace": ["epic", "historical", "philosophical"],
    "The Great Gatsby": ["tragic", "Roaring Twenties", "symbolic"],
    "One Hundred Years of Solitude": ["magical realism", "multi-generational", "poetic"],
    "Crime and Punishment": ["psychological", "moral conflict", "intense"],
    "The Alchemist": ["spiritual", "inspirational", "philosophical"],
    "Jane Eyre": ["gothic", "independent heroine", "romantic"],
    "Wuthering Heights": ["dark", "romantic", "gothic"],
    "Brave New World": ["dystopian", "satirical", "futuristic"],
    "The Catcher in the Rye": ["coming-of-age", "rebellious", "introspective"],
    "Anna Karenina": ["tragic", "romantic", "realist"],
    "Ulysses": ["modernist", "complex", "innovative"],
    "Don Quixote": ["adventurous", "parody", "classic"],
    "Frankenstein": ["gothic", "scientific", "tragic"],
    "Dracula": ["gothic", "horror", "vampiric"],
    "Fahrenheit 451": ["dystopian", "censorship", "thought-provoking"],
    "Lolita": ["controversial", "narrative style", "psychological"],
    "A Tale of Two Cities": ["historical", "sacrifice", "revolutionary"],
    "The Brothers Karamazov": ["philosophical", "family", "existential"],
    "Great Expectations": ["coming-of-age", "Victorian", "ambitious"],
    "Les Misérables": ["redemption", "historical", "social justice"],
    "The Odyssey": ["epic", "adventurous", "mythic"],
    "The Iliad": ["epic", "war", "mythic"],
    "Little Women": ["family", "coming-of-age", "feminist"],
    "Catch-22": ["satirical", "war", "absurd"],
    "Slaughterhouse-Five": ["anti-war", "sci-fi", "absurdist"],
    "The Grapes of Wrath": ["social realism", "migration", "family"],
    "Maus": ["graphic novel", "holocaust", "memoir"],
    "The Hobbit": ["adventure", "fantasy", "classic"],
    "The Handmaid’s Tale": ["dystopian", "feminist", "political"],
    "A Passage to India": ["colonialism", "cross-cultural", "philosophical"],
    "The Stranger": ["existential", "absurdist", "philosophical"],
    "Dune": ["epic", "sci-fi", "political intrigue"],
    "Beloved": ["historical", "magical realism", "trauma"],
    "Invisible Man": ["identity", "race", "surreal"],
    "The Picture of Dorian Gray": ["gothic", "aestheticism", "dark"],
    "Dr. Jekyll and Mr. Hyde": ["dual nature", "gothic", "psychological"],
    "The Count of Monte Cristo": ["revenge", "adventure", "redemption"],
    "Gone with the Wind": ["historical", "romantic", "Southern US"],
    "Rebecca": ["mystery", "gothic", "romantic suspense"],
    "Middlemarch": ["Victorian", "social commentary", "realist"],
    "East of Eden": ["family", "allegorical", "California"],
    "On the Road": ["beat generation", "adventurous", "countercultural"],
    "The Old Man and the Sea": ["existential", "struggle", "symbolic"],
    "Charlotte’s Web": ["children’s", "friendship", "heartwarming"],
    "The Wind-Up Bird Chronicle": ["surreal", "Japanese", "mysterious"],
}

ALL_DB = {
    "music": MUSIC_TAGS,
    "movies": MOVIE_TAGS,
    "painters": PAINTER_TAGS,
    "architecture": ARCHITECTURE_TAGS,
    "books": BOOK_TAGS
}


def load_profile(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_tags(category, items):
    db = ALL_DB.get(category, {})
    tags = []
    for item in items:
        tags.extend(db.get(item, []))
    return tags


def summarize(tags):
    counter = Counter(tags)
    if not counter:
        return "No recognizable items provided."
    top = counter.most_common(5)
    traits = ", ".join([f"{t} ({c})" for t, c in top])
    summary = fill(
        "Based on your selections, your taste gravitates toward "
        f"{', '.join([t for t, _ in top[:3]])}. "
        "These qualities suggest you value artists and works that are "
        f"{', '.join([t for t, _ in top])}.",
        width=80,
    )
    return summary + "\n\nTag counts: " + traits


def prompt_profile():
    """Interactively collect favorites for each category."""
    profile = {}
    for category, db in ALL_DB.items():
        print(f"\nSelect 5-10 items from {category.title()}. Enter numbers separated by commas:")
        items = list(db.keys())
        for i, name in enumerate(items, 1):
            print(f"{i}. {name}")
        raw = input("Your choices: ")
        selected = []
        for part in raw.split(','):
            part = part.strip()
            if part.isdigit():
                idx = int(part) - 1
                if 0 <= idx < len(items):
                    selected.append(items[idx])
        profile[category] = selected[:10]
    return profile


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Create an emotional portrait based on favorites")
    parser.add_argument("profile", nargs="?", help="Optional path to JSON file containing your selections")
    args = parser.parse_args()

    if args.profile:
        profile = load_profile(args.profile)
    else:
        profile = prompt_profile()
    all_tags = []
    for category, items in profile.items():
        all_tags.extend(collect_tags(category, items))
    print(summarize(all_tags))


if __name__ == "__main__":
    main()
