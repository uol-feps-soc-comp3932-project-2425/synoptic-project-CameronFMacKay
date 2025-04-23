
from backend.matching.gentag import generate_tag_from_image_context_automated
import pytest


def test_generate_tag_from_image_context_automated():
    dummy_input = {
        "image": "forest",
        "brightness": 180,
        "contrast": 60,
        "blur_score": 300,
        "colors": [{"name": "green", "percentage": 35}, {"name": "brown", "percentage": 25}],
        "composition": {
            "aspect_ratio": 1.2,
            "rule_of_thirds_score": 0.85,
            "symmetry_score": 0.75
        }
    }
    tag = generate_tag_from_image_context_automated(dummy_input)
    assert isinstance(tag, str)
    assert "forest" in tag
    assert "green" in tag or "brown" in tag
    assert any(term in tag for term in ["artistic", "symmetrical", "cinematic", "intimate", "dreamy", "relaxed", "vibrant"])
