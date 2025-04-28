[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zqYhAx1c)

# Machine Learning for Scene Classification and Environment-Driven Song Selection

This project uses **machine learning** and **natural language processing** to recommend songs based on the content of an uploaded image.  
It classifies the image environment (e.g., beach, nightclub), analyses visual features (e.g., brightness, dominant colours), and matches the scene to song lyrics using semantic similarity search.

Built using:
- Python (FastAPI backend)
- React (frontend)
- PyTorch (EfficientNet-B0 image classifier)
- Sentence-BERT (NLP for lyrics matching)
- FAISS (vector search for 10,000+ songs)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/uol-feps-soc-comp3932-project-2425/synoptic-project-CameronFMacKay.git
cd synoptic-project-CameronFMacKay
```


### 2. Backend Setup (FastAPI)

Navigate to the backend folder:

```bash
cd backend
```
---
Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run the backend server:

```bash
uvicorn main:app --reload
```

The FastAPI server will start at:  
`http://127.0.0.1:8000`

---

### 3. Frontend Setup (React)

Navigate to the frontend folder:

```bash
cd ../frontend
```

Install JavaScript dependencies:

```bash
npm install
```

Run the React development server:

```bash
npm start
```

The frontend will be accessible at:  
`http://localhost:3000`

---

### 4. Environment Requirements

- Python 3.10+
- Node.js 18+
- (Optional) CUDA-enabled GPU for local model retraining or MPS if using Applie silicon.
- Spotify Premium account (for song previews)

---





## 🧪 Frontend Testing Overview

Frontend component testing was implemented using [Vitest](https://vitest.dev/) to ensure correct UI behaviour and data handling within the React application.

| **Component**       | **Test File**         | **Purpose**                             | **Explanation**                                                                 |
|---------------------|------------------------|------------------------------------------|---------------------------------------------------------------------------------|
| `App.jsx`           | `App.test.jsx`         | Main layout and component composition    | Validates that all core UI components render correctly and receive props/data. |
| `Lyrics.jsx`        | `Lyrics.test.jsx`      | Song lyrics analysis display             | Tests fallback behaviour and rendering of lyrics, song info, and highlights.   |
| `Spotify.jsx`       | `Spotify.test.jsx`     | Spotify player and track info display    | Ensures song details, fallback UI, and Spotify iframe render as expected.      |
| `FileUpload.jsx`    | `FileUpload.test.jsx`  | Image upload handling                    | Tests file input logic and image preview rendering after selection.            |


## 🧪  Backend Testing Overview

The following unit tests were implemented using `pytest` to validate the functionality and correctness of the backend system components.

| **Test Name**                           | **Purpose**                           | **Explanation**                                                                 |
|----------------------------------------|---------------------------------------|---------------------------------------------------------------------------------|
| `test_image_analysis_output_keys`      | Check output structure of analysis    | Ensures the `image_analysis` function returns all expected keys.              |
| `test_colour_distribution_output`      | Validate HSV analysis output          | Tests that saturation, brightness levels, and colour data are in correct format.|
| `test_composition_output_format`       | Validate composition metadata         | Ensures return structure includes rule-of-thirds and symmetry metrics.         |
| `test_model_loading_places`            | Model loading check                   | Confirms EfficientNet model loads and is a `torch.nn.Module` instance.         |
| `test_prediction_output_places`        | Scene prediction logic                | Validates that the model can process an image and return a scene label.        |
| `test_enrich_tag_basic`                | Tag generation from base context      | Checks that synonyms and context attributes are added correctly.               |
| `test_generate_tag_from_image_context` | Automated tag generation              | Validates full image data converts to a semantic tag string.                   |
| `test_upload_endpoint`                 | Upload API interaction                | Tests `/upload` FastAPI endpoint, including handling of invalid image input.   |
| `test_spotify_search_endpoint`         | Spotify API wrapper validation        | Confirms `/api/spotify/search` returns a track list for valid queries.         |


