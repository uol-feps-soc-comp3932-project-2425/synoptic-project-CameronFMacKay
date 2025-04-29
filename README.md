# Machine Learning for Scene Classification and Environment-Driven Song Selection

This project uses **machine learning** and **natural language processing** to recommend songs based on the content of an uploaded image.  
It classifies the image environment (e.g., beach, nightclub), analyses visual features (e.g., brightness, dominant colours), and matches the scene to song lyrics using semantic similarity search.

## Disclaimer

This project was developed as part of a dissertation and uses several forms of AI. Please keep in mind that AI can make mistakes, and music recommendations are subjective to the individual. You use this tool at your own risk. For any issues or concerns, please contact sc21cm@leeds.ac.uk.

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


## External Materials

### Places365 Dataset
Zhou, B., Lapedriza, A., Khosla, A., Oliva, A. and Torralba, A., 2018. Places: A 10 million image database for scene recognition. [online] MIT CSAIL. Available at: http://places2.csail.mit.edu  [Accessed 20 Apr. 2025].
### Top 10,000 Spotify Songs Dataset
Beach, J., 2023. Top 10,000 Spotify Songs (1950–Now). [online] Kaggle. Available at: https://www.kaggle.com/datasets/joebeachcapital/top-10000-spotify-songs-1960-now [Accessed 28 Mar. 2025].
Machine Learning Models and Libraries
### EfficientNet-B0 (Image Classification)
Tan, M. and Le, Q., 2019. EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. In: International Conference on Machine Learning (ICML). [online] Available at: https://arxiv.org/abs/1905.11946 [Accessed 15 Mar. 2025].
### Sentence-BERT (all-MiniLM-L6-v2)
Reimers, N. and Gurevych, I., 2019. Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In: Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP). [online] Available at: https://arxiv.org/abs/1908.10084 [Accessed 20 Mar. 2025].
### WordNet
Miller, G.A., 1995. WordNet: A lexical database for English. Communications of the ACM, 38(11), pp.39–41. [online] Available at: https://wordnet.princeton.edu  [Accessed 20 Apr. 2025].
APIs and Tools
### Genius API
Genius, 2025. Genius API for lyrics metadata. [online] Available at: https://docs.genius.com/  [Accessed 22 Mar. 2025].
### Spotify Web API
Spotify for Developers, 2025. Spotify Web API. [online] Available at: https://developer.spotify.com/documentation/web-api [Accessed 22 Mar. 2025].
### FAISS (Facebook AI Similarity Search)
Johnson, J., Douze, M. and Jégou, H., 2019. Billion-scale similarity search with GPUs. IEEE Transactions on Big Data, 7(3), pp.535–547. [online] Available at: https://faiss.ai [Accessed 25 Mar. 2025].
