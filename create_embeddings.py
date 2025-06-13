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

total_docs = collection.count_documents({})

#--------------------------------------------------

c = 1
number = 100
start_time = time.time()
total_elapsed = 0

for doc in collection.find({'plot': {"$exists": True}}).limit(total_docs):

    doc[name_field] = generate_embedding(doc['plot'])
    collection.replace_one({'_id': doc['_id']}, doc)

    if (c % number) == 0:

        end_time = time.time()
        elapsed = end_time - start_time
        start_time = end_time
        percentage = round((c/total_docs)*100, 2)
        total_elapsed = total_elapsed + elapsed

        print(f"Number of documents: {c}/{total_docs}")
        print(f"Percentage of documents: {percentage}%")
        print(f"Particular iteration: {format_time(elapsed)}")
        print(f"Accumulated time: {format_time(total_elapsed)}")
        print('-'*40)

    c = c + 1

#--------------------------------------------------