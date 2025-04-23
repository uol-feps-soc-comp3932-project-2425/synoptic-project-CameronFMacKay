
import os
import numpy as np
import cv2
import pytest
from backend.images.imageanalysis import image_analysis, analyze_color_distribution, detect_composition

# Create a dummy image to test with
@pytest.fixture(scope="module")
def dummy_image_path(tmp_path_factory):
    img = np.full((256, 256, 3), fill_value=(100, 150, 200), dtype=np.uint8)
    path = tmp_path_factory.mktemp("data") / "dummy.jpg"
    cv2.imwrite(str(path), img)
    return str(path)

def test_image_analysis_output_keys(dummy_image_path):
    details = image_analysis(dummy_image_path)
    expected_keys = {'brightness', 'contrast', 'blur_score', 'colors', 'composition'}
    assert expected_keys.issubset(details.keys())

def test_color_distribution_output_format(dummy_image_path):
    img = cv2.imread(dummy_image_path)
    result = analyze_color_distribution(img)
    assert isinstance(result, dict)
    assert 'hsv_means' in result
    assert 'saturation_level' in result
    assert 'brightness_level' in result

def test_composition_output_format(dummy_image_path):
    img = cv2.imread(dummy_image_path)
    result = detect_composition(img)
    assert 'aspect_ratio' in result
    assert 'rule_of_thirds_score' in result
    assert 'symmetry_score' in result
    assert isinstance(result['grid_brightness'], list)
