import numpy as np
import os
from functools import lru_cache

# Global cache for WordNet data
WORDNET_CACHE = {}

@lru_cache(maxsize=128)
def get_similar_words(word, max_results=3):
    """
    Get semantically similar words using WordNet with caching.
    """
    try:
        import nltk
        from nltk.corpus import wordnet
        
        # Ensure WordNet is downloaded only once
        if not hasattr(get_similar_words, '_nltk_downloaded'):
            try:
                nltk.data.find('corpora/wordnet')
            except LookupError:
                nltk.download('wordnet', quiet=True)
            get_similar_words._nltk_downloaded = True
        
        if word in WORDNET_CACHE:
            return WORDNET_CACHE[word]
            
        synsets = wordnet.synsets(word)
        if not synsets:
            return []
            
        similar_words = []
        for synset in synsets[:2]:  # Consider top 2 meanings
            for lemma in synset.lemmas():
                similar_words.append(lemma.name().replace('_', ' '))
            
            # Only get hypernyms and hyponyms if we don't have enough words yet
            if len(similar_words) < max_results:
                for hyponym in synset.hyponyms()[:1]:
                    if hyponym.lemmas():
                        similar_words.append(hyponym.lemmas()[0].name().replace('_', ' '))
                
                for hypernym in synset.hypernyms()[:1]:
                    if hypernym.lemmas():
                        similar_words.append(hypernym.lemmas()[0].name().replace('_', ' '))
        
        # Remove duplicates while preserving order
        unique_similar = []
        for word in similar_words:
            if word not in unique_similar:
                unique_similar.append(word)
                
        result = unique_similar[:max_results]
        WORDNET_CACHE[word] = result
        return result
    except ImportError:
        # Handle case where nltk is not available
        return []

def get_color_term(r, g, b):
    """Determine color term based on RGB values."""
    if max(r, g, b) < 50:  # Very dark
        return "night"
    elif r > g and r > b:  # Red dominant
        return "passion" if r > 150 else "warmth"
    elif g > r and g > b:  # Green dominant
        return "nature" if g > 150 else "forest"
    elif b > r and b > g:  # Blue dominant
        return "sky" if b > 150 else "ocean"
    elif r > 200 and g > 200 and b > 200:  # White/very bright
        return "clarity"
    return ""

def get_mood_descriptor(brightness, contrast):
    """Get mood descriptor based on brightness and contrast."""
    # Normalize values to 0-1 range if they're in the 0-255 range
    b_norm = brightness / 255 if brightness > 1 else brightness
    c_norm = contrast / 255 if contrast > 1 else contrast
    
    # Use a lookup table for faster determination
    if b_norm > 0.7:  # Bright
        return "vibrant" if c_norm > 0.5 else "airy"
    elif b_norm > 0.4:  # Medium
        return "energetic" if c_norm > 0.6 else "relaxed"
    else:  # Dark
        return "intense" if c_norm > 0.5 else "moody"

def generate_tag_from_image_context_automated(image_data):
    descriptors = []

    # Process primary image tag
    image_tag = image_data.get("image", "")
    base_words = image_tag.replace("_", " ").split()
    descriptors.extend(base_words)
    for word in base_words:
        descriptors.extend(get_similar_words(word))

    # Mood from brightness and contrast
    brightness = image_data.get("brightness", 0)
    contrast = image_data.get("contrast", 0)
    mood = get_mood_descriptor(brightness, contrast)
    descriptors.append(mood)
    descriptors.extend(get_similar_words(mood, max_results=2))

    # Blur score for atmosphere
    blur_score = image_data.get("blur_score", 0)
    # if blur_score > 600:
        
        # descriptors.append("dreamy")
        # descriptors.append("nostalgic")
    if blur_score > 400:
        descriptors.append("soft")
    elif blur_score < 200:
        descriptors.append("sharp")
        descriptors.append("realistic")
    else:
        descriptors.append("subtle")
    
    if brightness > 100:
        descriptors.append("bright")
    elif brightness < 50:
        descriptors.append("dark")

    # Use top 2 dominant colors
    if "colors" in image_data:
        top_colors = sorted(image_data["colors"], key=lambda c: c["percentage"], reverse=True)[:2]
        for color in top_colors:
            color_name = color["name"].lower()
            descriptors.append(color_name)
            descriptors.extend(get_similar_words(color_name, max_results=1))

    # Aspect ratio
    ar = image_data.get("composition", {}).get("aspect_ratio", 1)
    if ar > 1.6:
        descriptors.append("cinematic")
    elif ar < 1.1:
        descriptors.append("intimate")

    # Rule of Thirds & Symmetry
    composition = image_data.get("composition", {})
    if composition.get("rule_of_thirds_score", 0) > 0.8:
        descriptors.append("artistic")
    if composition.get("symmetry_score", 0) > 0.7:
        descriptors.append("symmetrical")

    # Final deduplication and selection
    unique_descriptors = []
    seen = set()
    for d in descriptors:
        if d and d not in seen:
            unique_descriptors.append(d)
            seen.add(d)

    # Trim or adjust weight if needed
    final_descriptors = unique_descriptors[:10]

    return " ".join(final_descriptors)
