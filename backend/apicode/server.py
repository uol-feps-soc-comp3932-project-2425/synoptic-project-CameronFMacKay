from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import sys

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../images'))
sys.path.append(module_path)

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../matching'))
sys.path.append(module_path)
import imageanalysis
import places
import tagfunction

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
    tag = tagfunction.main(image)
    print(tag)
    results['image'] = image
    results['tag'] = tag
    return JSONResponse(content={"message": "File uploaded successfully", "filename": file.filename, "image_data" : results})


@app.get('/hello/')
async def api_check():
    return JSONResponse(content={"message": "hello from server.py"})