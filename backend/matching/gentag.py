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
    """
    Generate a descriptive tag for song matching based on image context data,
    using WordNet to find semantically similar words automatically.
    
    Args:
        image_data (dict): Dictionary containing image context data including:
            - brightness (float): The brightness value of the image (0-255 scale)
            - contrast (float): The contrast value of the image (0-255 scale)
            - main_colour (list): RGB values of the main color
            - second_colour (list): RGB values of the secondary color (can be None)
            - image (str): The image classification tag
    
    Returns:
        str: A descriptive tag that can be used to find similar songs
    """
    # Initialize base descriptors with a reasonable capacity to avoid resizing
    descriptors = []
    
    # Process the image classification tag
    if "image" in image_data and image_data["image"]:
        image_tag = image_data["image"]
        
        # Split compound tags more efficiently
        base_words = image_tag.replace("_", " ").split()
        descriptors.extend(base_words)
        
        # Find semantically similar words using WordNet - batch process to reduce overhead
        for word in base_words:
            similar_words = get_similar_words(word)
            descriptors.extend(similar_words)
    
    # Process brightness and contrast to add mood descriptors
    if "brightness" in image_data and "contrast" in image_data:
        mood_descriptor = get_mood_descriptor(image_data["brightness"], image_data["contrast"])
        descriptors.append(mood_descriptor)
        
        # Add similar mood words
        mood_similar = get_similar_words(mood_descriptor, max_results=2)
        if mood_similar:
            descriptors.extend(mood_similar)
    
    # Process main color to add color-related context
    color_term = ""
    if "main_colour" in image_data and image_data["main_colour"]:
        r, g, b = image_data["main_colour"]
        color_term = get_color_term(r, g, b)
        
        if color_term:
            # Find related words to color term
            color_related = get_similar_words(color_term, max_results=1)
            if color_related:
                descriptors.extend(color_related)
    
    # Use a set to efficiently remove duplicates, then convert back to list
    unique_descriptors = []
    seen = set()
    for d in descriptors:
        if d and d not in seen:
            unique_descriptors.append(d)
            seen.add(d)
    
    # Limit to top N most relevant terms
    max_terms = 8
    final_descriptors = unique_descriptors[:max_terms]
    
    # Add color term if it exists and not already in the list
    if color_term and color_term not in seen and len(final_descriptors) < max_terms:
        final_descriptors.append(color_term)
    
    # Join descriptors into a tag
    tag = " ".join(final_descriptors)
    
    return tag