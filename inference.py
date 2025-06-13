import os
import time
import pymongo
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

#--------------------------------------------------

def generate_embedding(text: str) -> list[float]:
    return model.encode(text).tolist()


def format_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours}h {minutes}m {secs:.2f}s"


def build_prompt(user_prompt: str, movies: list) -> str:
    movie_descriptions = "\n".join(
        [f"Title: {m['title']}\nDescription: {m['plot']}\n{'-' * 70}" for m in movies]
    )

    base_prompt = f"""You are a film expert with deep knowledge of all movies. 
Your task is to help a screenwriter friend create the theme for their next story.

This friend gives you an initial concept they want to develop:

user_prompt = "{user_prompt}"

To inspire your answer, consider the following existing films, paying close attention to their settings,
 dynamics, and human conflicts:

{movie_descriptions}

Your goal is to:
- Identify thematic, historical, or emotional patterns across the listed films.
- Propose an original story theme inspired by those patterns but not directly copying any of them.

Provide a **concise and compelling thematic description**, suitable for kicking off a screenplay 
or film project pitch.
"""
    return base_prompt


def creation_enriched_prompt(query):
    
    results = collection.aggregate([
        {"$vectorSearch": {
            "queryVector": generate_embedding(query),
            "path": name_field,
            "numCandidates": 100,
            "limit": 10,
            "index": name_vector_search,
        }}
    ])

    movies = []

    for document in results:
        movies.append(document)

    return build_prompt(query, movies)

#--------------------------------------------------

# Load the environment variables
load_dotenv()

user_name = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")

#--------------------------------------------------

url_connect = f"mongodb+srv://{user_name}:{password}@cluster0.fb30e3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

embedding_model = "sentence-transformers/all-MiniLM-L6-v2"

name_field = 'plot_embedding_hf'
name_vector_search = "embedding_description"

#--------------------------------------------------

client = pymongo.MongoClient(url_connect)

db = client.sample_mflix
collection = db.movies

model = SentenceTransformer(embedding_model)

#--------------------------------------------------

query = (
    "I want you to create a theme centered around a brutal medieval battle "
    "between two rival kingdoms, highlighting the emotional and political costs of war."
)

print(creation_enriched_prompt(query))

#--------------------------------------------------