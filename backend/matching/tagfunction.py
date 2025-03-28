import faiss
import sqlite3
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
import re

def search_songs(tag, top_k, model, device):
    tag_embedding = model.encode([tag], convert_to_numpy=True, device=device)
    index = faiss.read_index("../matching/song_lyrics4.index")
    distances, indices = index.search(tag_embedding, top_k)
    # Retrieve song metadata
    db_conn = sqlite3.connect("../matching/songs4.db")
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

def analyze_lyrics_matches(tag, lyrics, model, device):
    """
    Analyze lyrics to identify words/phrases that match the tag.
    Returns lyrics with highlighting data for the frontend.
    """
    # Split lyrics into sentences or lines
    lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
    
    # Get embedding for the tag
    tag_embedding = model.encode([tag], convert_to_numpy=True, device=device)[0]
    
    # Process each line to find matching words
    processed_lyrics = []
    
    for line in lines:
        # Split into words, preserving punctuation
        words = re.findall(r'\b\w+\b|\S', line)
        
        # Create word groups (individual words and small phrases)
        word_groups = []
        for i in range(len(words)):
            # Single words
            word_groups.append((" ".join(words[i:i+1]), i, i))
            
            # 2-word phrases if possible
            if i < len(words) - 1:
                word_groups.append((" ".join(words[i:i+2]), i, i+1))
                
            # 3-word phrases if possible
            if i < len(words) - 2:
                word_groups.append((" ".join(words[i:i+3]), i, i+2))
        
        # Get embeddings for word groups that have actual content
        content_groups = [(phrase, start, end) for phrase, start, end in word_groups if re.search(r'\w', phrase)]
        if not content_groups:
            processed_lyrics.append({"text": line, "words": []})
            continue
            
        phrases = [phrase for phrase, _, _ in content_groups]
        phrase_embeddings = model.encode(phrases, convert_to_numpy=True, device=device)
        
        # Calculate similarity scores
        similarities = np.dot(phrase_embeddings, tag_embedding) / (
            np.linalg.norm(phrase_embeddings, axis=1) * np.linalg.norm(tag_embedding)
        )
        
        # Create word match information
        word_matches = []
        for i, ((phrase, start, end), similarity) in enumerate(zip(content_groups, similarities)):
            # Categorize match strength
            match_strength = "none"
            if similarity > 0.6:
                match_strength = "strong" 
            elif similarity > 0.4:
                match_strength = "medium"
            elif similarity > 0.2:
                match_strength = "weak"
                
            if match_strength != "none":
                word_matches.append({
                    "phrase": phrase,
                    "start_idx": start,
                    "end_idx": end,
                    "similarity": float(similarity),
                    "strength": match_strength
                })
        
        # Group overlapping matches and keep only the strongest
        word_matches.sort(key=lambda x: x["similarity"], reverse=True)
        final_matches = []
        covered_indices = set()
        
        for match in word_matches:
            indices = set(range(match["start_idx"], match["end_idx"] + 1))
            if not indices.intersection(covered_indices):
                final_matches.append(match)
                covered_indices.update(indices)
        
        # Add to processed lyrics
        processed_lyrics.append({
            "text": line,
            "words": final_matches
        })
    
    return processed_lyrics

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
    # Process and return results with match highlighting
    if results:
        outputs = []
        for artist, title, lyrics, similarity in results:
            # Analyze lyrics to find matches
            processed_lyrics = analyze_lyrics_matches(tag, lyrics, model, device)
            
            output = {
                'artist': artist,
                'title': title,
                'overall_similarity': float(similarity),
                'lyrics': processed_lyrics  # Now contains highlighting data
            }
            outputs.append(output)
        
        return outputs
    else:
        return None