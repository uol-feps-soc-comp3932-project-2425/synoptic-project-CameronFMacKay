
import torch
from torchvision import transforms
from backend.images.places import classify_image
from PIL import Image
import pytest
import os

@pytest.fixture(scope="module")
def dummy_image_path(tmp_path_factory):
    img = Image.new("RGB", (256, 256), color='white')
    path = tmp_path_factory.mktemp("data") / "dummy.jpg"
    img.save(path)
    return str(path)

def test_classify_image(dummy_image_path):
    try:
        result = classify_image(dummy_image_path)
        assert isinstance(result, str)
        assert len(result) > 0
    except FileNotFoundError:
        pytest.skip("Model or classmapping.csv not found. Skipping test.")
    except Exception as e:
        pytest.fail(f"Unexpected error during classification: {e}")
