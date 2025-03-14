import cv2
import numpy as np
from sklearn.cluster import KMeans
import webcolors

def rgb_to_color_name(rgb):
    try:
        # Get the closest color name for the given RGB value
        color_name = webcolors.rgb_to_name(rgb)
        return color_name
    except ValueError:
        return None
    

def image_analysis(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError('Image Not Found')
    
    pixels = image.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(pixels)
    
    dominant_colours = kmeans.cluster_centers_.astype(int)
    
    labels = kmeans.labels_
    
    unique, counts = np.unique(labels, return_counts=True)
    
    dominance_scores = dict(zip(unique, counts / len(labels) * 100))  # in percentage
    
    sorted_scores = sorted(dominance_scores.items(), key=lambda x: x[1], reverse=True)
    
    most_dominant_colour = dominant_colours[sorted_scores[0][0]]
    second_dominant_colour = dominant_colours[sorted_scores[1][0]]
    
    if abs(sorted_scores[0][1] - sorted_scores[1][1]) > 20:
        second_dominant_colour = None

    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    name = rgb_to_color_name((most_dominant_colour[0],most_dominant_colour[1],most_dominant_colour[2]))
    details ={
        'brightness' : float(np.mean(grey_img)), # 0 black 255 white
        'contrast' : float(np.std(grey_img)), # 0 little contrast 255 high contrast 
        'main_colour' : most_dominant_colour.tolist(),
        'second_colour': second_dominant_colour.tolist() if second_dominant_colour is not None else None

    }

    return details