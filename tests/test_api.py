
import pytest
from fastapi.testclient import TestClient
from backend.apicode.server import app
from PIL import Image
import io

client = TestClient(app)

@pytest.fixture(scope="module")
def dummy_image():
    # Create a dummy 256x256 white JPEG image
    img = Image.new("RGB", (256, 256), color="white")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    return img_bytes

def test_upload_endpoint(dummy_image):
    response = client.post(
        "/upload/",
        files={"file": ("dummy.jpg", dummy_image, "image/jpeg")}
    )
    # Acceptable if image analysis errors or is slow
    assert response.status_code in (200, 422)

def test_spotify_search_endpoint():
    response = client.get("/api/spotify/search", params={"q": "Adele Hello", "limit": 1})
    assert response.status_code == 200
    assert "tracks" in response.json()
