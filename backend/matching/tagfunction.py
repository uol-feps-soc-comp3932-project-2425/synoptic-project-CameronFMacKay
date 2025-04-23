import faiss
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
import re
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'matching'))
index_path = os.path.join(BASE_DIR, "song_lyrics4.index")
db_path = os.path.join(BASE_DIR, "songs4.db")

def search_songs(tag, top_k, model, device):
    tag_embedding = model.encode([tag], convert_to_numpy=True, device=device)
    index = faiss.read_index(index_path)
    distances, indices = index.search(tag_embedding, top_k)
    db_conn = sqlite3.connect(db_path)
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
    lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
    
    tag_embedding = model.encode([tag], convert_to_numpy=True, device=device)[0]
    
    processed_lyrics = []
    
    for line in lines:
        words = re.findall(r'\b\w+\b|\S', line)
        
        word_groups = []
        for i in range(len(words)):
            word_groups.append((" ".join(words[i:i+1]), i, i))
            
            if i < len(words) - 1:
                word_groups.append((" ".join(words[i:i+2]), i, i+1))
                
            if i < len(words) - 2:
                word_groups.append((" ".join(words[i:i+3]), i, i+2))
        
        content_groups = [(phrase, start, end) for phrase, start, end in word_groups if re.search(r'\w', phrase)]
        if not content_groups:
            processed_lyrics.append({"text": line, "words": []})
            continue
            
        phrases = [phrase for phrase, _, _ in content_groups]
        phrase_embeddings = model.encode(phrases, convert_to_numpy=True, device=device)
        
        similarities = np.dot(phrase_embeddings, tag_embedding) / (
            np.linalg.norm(phrase_embeddings, axis=1) * np.linalg.norm(tag_embedding)
        )
        
        word_matches = []
        for i, ((phrase, start, end), similarity) in enumerate(zip(content_groups, similarities)):
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
        
        word_matches.sort(key=lambda x: x["similarity"], reverse=True)
        final_matches = []
        covered_indices = set()
        
        for match in word_matches:
            indices = set(range(match["start_idx"], match["end_idx"] + 1))
            if not indices.intersection(covered_indices):
                final_matches.append(match)
                covered_indices.update(indices)
        
        processed_lyrics.append({
            "text": line,
            "words": final_matches
        })
    
    return processed_lyrics

def main(image):
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = SentenceTransformer("all-MiniLM-L6-v2").to(device)
    tag = image
    top_k = 5
    results = search_songs(tag, top_k, model, device)
    if results:
        outputs = []
        for artist, title, lyrics, similarity in results:
            processed_lyrics = analyze_lyrics_matches(tag, lyrics, model, device)
            
            output = {
                'artist': artist,
                'title': title,
                'overall_similarity': float(similarity),
                'lyrics': processed_lyrics
            }
            outputs.append(output)
        
        return outputs
    else:
        return None