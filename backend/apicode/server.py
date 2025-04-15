from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import base64
import sys

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../images'))
sys.path.append(module_path)

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../matching'))
sys.path.append(module_path)
import imageanalysis
import places
import tagfunction
import gentag
import requests
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.abspath(os.path.join(UPLOAD_DIR, file.filename))
    print(file_location)
    # Save the uploaded file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    results = imageanalysis.image_analysis(file_location)
    image = places.classify_image(file_location)
    results['image'] = image
    output = gentag.generate_tag_from_image_context_automated(results)
    print(output)
    tag = tagfunction.main(output)
    results['tag'] = tag
    return JSONResponse(content={"message": "File uploaded successfully", "filename": file.filename, "image_data" : results})


@app.get('/hello/')
async def api_check():
    return JSONResponse(content={"message": "hello from server.py"})


# Spotify API credentials
SPOTIFY_CLIENT_ID =     "2302d67b9bb74991a81691f7349acfe2"
SPOTIFY_CLIENT_SECRET = "d52bb27ff7164224a5bbbd8d247285e3"

# Token storage
token_info = {
    "access_token": None,
    "expires_at": 0
}

class SpotifyTrack(BaseModel):
    id: str
    name: str
    artists: List[Dict[str, Any]]
    album: Dict[str, Any]
    external_urls: Dict[str, str]
    preview_url: Optional[str] = None

class SearchResponse(BaseModel):
    tracks: List[SpotifyTrack]
    query: str

async def get_spotify_token():
    """Get a new Spotify access token using client credentials flow"""
    import time
    
    # Check if we already have a valid token
    if token_info["access_token"] and token_info["expires_at"] > time.time():
        return token_info["access_token"]
    
    # Prepare the request
    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    url = "https://accounts.spotify.com/api/token"
    
    # Make the request
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to get Spotify token: {response.text}"
        )
    
    # Parse the response
    response_data = response.json()
    token_info["access_token"] = response_data["access_token"]
    token_info["expires_at"] = time.time() + response_data["expires_in"] - 60  # Expire 60 seconds early to be safe
    
    return token_info["access_token"]

@app.get("/api/spotify/search", response_model=SearchResponse)
async def search_spotify_track(
    q: str = Query(..., description="Search query (e.g., 'title artist:name')"),
    limit: int = Query(1, description="Number of results to return")
):
    """
    Search for tracks on Spotify and return their details.
    The query format can be 'title artist:name' for better results.
    """
    # Get access token
    token = await get_spotify_token()
    
    # Prepare the search request
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": q,
        "type": "track",
        "limit": limit
    }
    
    # Make the request
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Spotify search failed: {response.text}"
        )
    
    # Parse the response
    response_data = response.json()
    
    if not response_data["tracks"]["items"]:
        return {"tracks": [], "query": q}
    
    # Extract the relevant track information
    tracks = []
    for item in response_data["tracks"]["items"]:
        track = {
            "id": item["id"],
            "name": item["name"],
            "artists": [{"id": artist["id"], "name": artist["name"]} for artist in item["artists"]],
            "album": {
                "id": item["album"]["id"],
                "name": item["album"]["name"],
                "images": item["album"]["images"]
            },
            "external_urls": item["external_urls"],
            "preview_url": item["preview_url"]
        }
        tracks.append(track)
    
    return {"tracks": tracks, "query": q}