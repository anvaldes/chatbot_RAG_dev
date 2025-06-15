# 🎬 Semantic Movie Prompt Generator using MongoDB & Sentence Transformers

This project enriches user-provided **screenwriting prompts** with **semantic context** from a movie database.  
It leverages **sentence-transformers** and **MongoDB Atlas Vector Search** to create intelligent, original story ideas.

---

## ✨ Features

- Embeds movie plots using `sentence-transformers/all-MiniLM-L6-v2`
- Stores and retrieves vectors from MongoDB Atlas with `$vectorSearch`
- Automatically builds detailed prompts for story ideation
- Uses the `sample_mflix.movies` collection
- Modular scripts for **embedding** and **inference**

---

## 🧠 How It Works

1. **Embedding**  
   The `create_embeddings.py` script:
   - Connects to MongoDB Atlas
   - Embeds the `plot` field from each movie
   - Stores the embeddings in a new field (`plot_embedding_hf`)

2. **Inference**  
   The `inference.py` script:
   - Takes a user prompt (e.g., "epic medieval war")
   - Finds the top 10 semantically similar movies using `$vectorSearch`
   - Generates a rich, structured prompt combining those films with the user's idea

---

## 🔧 Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file:

```
USER_NAME=your_mongodb_user
PASSWORD=your_mongodb_password
```

---

## 🚀 Running the Embedding Script

```bash
python create_embeddings.py
```

This will iterate over all documents with a `plot`, generate embeddings, and update them in the MongoDB database.

---

## 🔍 Running the Prompt Generator

```bash
python inference.py
```

You can modify the `query` at the bottom of `inference.py` to test other story ideas.

Example:

```python
query = "A cyberpunk heist in a dystopian city controlled by rogue AIs"
```

---

## 📦 Dependencies

Main libraries used:

```
pymongo
sentence-transformers
python-dotenv
```

---
