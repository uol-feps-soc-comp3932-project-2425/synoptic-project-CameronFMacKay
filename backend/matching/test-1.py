# %%
from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load a model for semantic similarity
model = SentenceTransformer("all-MiniLM-L6-v2")  # Small, fast & effective


# %%
df = pd.read_csv('songs_lyrics_adjusted.csv')


# %%
df.head()

# %%
newdf = df[["title", "lyrics"]]  # Keep necessary info

# Fill missing lyrics with an empty string to avoid errors
newdf["lyrics"] = newdf["lyrics"].fillna("")



# %%
testdf = newdf[0:1000]

# %%
import torch

# Set device to MPS if available, otherwise use CPU
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Example image tag from classified image
image_tag = "sad airport airplane"

# Generate image tag embedding and move it to MPS
image_tag_embedding = model.encode(image_tag, convert_to_tensor=True).to(device)

# %%




# Encode each song's metadata and store it as a NumPy array (on CPU)
testdf.loc[:,"song_embedding"] = testdf.apply(
    lambda row: model.encode(f"{row['title']} {row['lyrics']}", convert_to_tensor=True).cpu().numpy(),
    axis=1
)


# %%
# Compute similarity between image tag and each song


testdf.loc[:,"similarity"] = testdf["song_embedding"].apply(
    lambda emb: util.pytorch_cos_sim(image_tag_embedding, torch.tensor(emb, device=image_tag_embedding.device)).item()
)


# Find the best-matching song
best_match = testdf.loc[testdf["similarity"].idxmax()]
best_match_index = testdf["similarity"].idxmax()  # Get index of the best match
best_match = testdf.loc[best_match_index]  # Get the best match row

# Retrieve the artist from the original df using the same position
artist_name = df.iloc[best_match_index]["artist"]


# Print result
print(f"Best-matching song: {best_match['title']} by {artist_name} (Score: {best_match['similarity']:.4f})")



