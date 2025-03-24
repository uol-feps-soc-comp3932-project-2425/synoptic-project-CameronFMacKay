import faiss
import sqlite3
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import torch


def search_songs(tag, top_k, model, device):
    tag_embedding = model.encode([tag], convert_to_numpy=True, device=device)
    index = faiss.read_index("../matching/song_lyrics.index")
    distances, indices = index.search(tag_embedding, top_k)
    # Retrieve song metadata
    db_conn = sqlite3.connect("../matching/songs.db")
    cursor = db_conn.cursor()
    
    results = []
    for idx, distance in zip(indices[0], distances[0]):
        cursor.execute("SELECT artist, title, lyrics FROM songs WHERE rowid = ?", (int(idx)+1,))
        row = cursor.fetchone()
        if row:
            artist, title, lyrics = row
            results.append((artist, title, lyrics, distance))
    
    db_conn.close()
    return results

def main(image):
    # Detect appropriate device
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    # Load the model
    model = SentenceTransformer("all-MiniLM-L6-v2").to(device)
    # Define search parameters
    tag = image
    top_k = 5
    # Search for songs
    results = search_songs(tag, top_k, model, device)
    # Display results
    if results:
        print("Most similar song:")
        artist, title, lyrics, similarity = results[0]
        print(artist)
        print(f"Title: {title}\nLyrics: {lyrics[:200]}...\nSimilarity Score: {similarity:.4f}\n")
        output = {
            'artist' : artist,
            'title' : title,
            'lyrics' : float(similarity)
        }
        return output
    else:
        return None
        
        
