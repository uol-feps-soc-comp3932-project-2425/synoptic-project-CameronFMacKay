import cv2
import numpy as np
from sklearn.cluster import KMeans
import webcolors
from collections import Counter
import math

def closest_color(rgb):
    min_colors = {}
    for name, hex_value in webcolors.CSS3_NAMES_TO_HEX.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_value)
        rd = (r_c - rgb[0]) ** 2
        gd = (g_c - rgb[1]) ** 2
        bd = (b_c - rgb[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    
    return min_colors[min(min_colors.keys())]

def rgb_to_color_name(rgb):
    try:
        return webcolors.rgb_to_name(rgb)
    except ValueError:
        return closest_color(rgb)



def analyze_color_distribution(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    h_mean, h_std = np.mean(hsv[:,:,0]), np.std(hsv[:,:,0])
    s_mean, s_std = np.mean(hsv[:,:,1]), np.std(hsv[:,:,1])
    v_mean, v_std = np.mean(hsv[:,:,2]), np.std(hsv[:,:,2])
    
    saturation_level = "high" if s_mean > 128 else "medium" if s_mean > 64 else "low"
    brightness_level = "bright" if v_mean > 180 else "medium" if v_mean > 100 else "dark"
    
    return {
        'hsv_means': [float(h_mean), float(s_mean), float(v_mean)],
        'hsv_std': [float(h_std), float(s_std), float(v_std)],
        'color_richness': float(s_mean * s_std / 255),
        'saturation_level': saturation_level,
        'brightness_level': brightness_level
    }

def detect_composition(image):
    height, width, _ = image.shape
    aspect_ratio = width / height
    
    h_step, w_step = height // 3, width // 3
    grid_brightness = []
    
    for i in range(3):
        row = []
        for j in range(3):
            cell = image[i*h_step:(i+1)*h_step, j*w_step:(j+1)*w_step]
            cell_gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
            row.append(float(np.mean(cell_gray)))
        grid_brightness.append(row)
    
    # Check if image follows rule of thirds
    intersection_points = [
        grid_brightness[0][0], grid_brightness[0][2],
        grid_brightness[2][0], grid_brightness[2][2]
    ]
    center_point = grid_brightness[1][1]
    
    rule_of_thirds_score = sum(intersection_points) / (4 * center_point) if center_point > 0 else 0
    
    return {
        'aspect_ratio': float(aspect_ratio),
        'grid_brightness': grid_brightness,
        'rule_of_thirds_score': float(rule_of_thirds_score),
        'symmetry_score': float(1 - abs(np.mean(grid_brightness[0]) - np.mean(grid_brightness[2])) / 255)
    }

def image_analysis(image_path, num_colors=5):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError('Image Not Found')
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image_rgb.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    
    dominant_colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    
    label_counts = Counter(labels)
    
    total_pixels = len(labels)
    color_percentages = {i: (count / total_pixels * 100) for i, count in label_counts.items()}
    
    sorted_colors = sorted(color_percentages.items(), key=lambda x: x[1], reverse=True)
    
    color_info = []
    for idx, (cluster_idx, percentage) in enumerate(sorted_colors):
        color = dominant_colors[cluster_idx].tolist()
        color_name = rgb_to_color_name(tuple(color))
        color_info.append({
            'rgb': color,
            'name': color_name,
            'percentage': float(percentage)
        })
    
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = float(np.mean(grey_img))
    contrast = float(np.std(grey_img))
    
    laplacian = cv2.Laplacian(grey_img, cv2.CV_64F)
    blur_score = float(np.var(laplacian))
    
    composition_features = detect_composition(image)
    
    details = {
        
        'brightness': brightness,  # 0 black 255 white
        'contrast': contrast,  # 0 little contrast 255 high contrast
        'blur_score': blur_score, # Lower values indicate more blur
        'colors': color_info,
        'composition': composition_features,
    }
    return details