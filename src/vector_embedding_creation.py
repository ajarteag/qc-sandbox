from PIL import Image
import numpy as np
import torch
from transformers import CLIPTokenizer, CLIPTextModelWithProjection
import pandas as pd
import os

# Device setup
torch_device = "cpu"

# Paths
csv_path = "food.csv"  # Update this with your actual CSV path
save_root = "./embedding_database/"

# Load tokenizer and model
print("Loading tokenizer and encoder...")
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
text_encoder = CLIPTextModelWithProjection.from_pretrained("openai/clip-vit-large-patch14")
text_encoder = text_encoder.to(torch_device).half()

# Read CSV
print(f"Reading CSV from {save_root + csv_path}...")
df = pd.read_csv(save_root + csv_path)
required_cols = {"ID", "name", "Food Group"}
if not required_cols.issubset(df.columns):
    raise ValueError(f"CSV must contain the following columns: {required_cols}")

text_embeddings = []
id_array = []

# Process each row
try: 
    print("Encoding rows...")
    for i, (_, row) in enumerate(df.iterrows()):
        text_input = f"{row['name']} {row['Food Group']}"
        tokenized = tokenizer(
            text_input,
            padding="max_length",
            max_length=tokenizer.model_max_length,
            truncation=True,
            return_tensors="pt"
        ).to(torch_device)

        with torch.no_grad():
            embedding = text_encoder(**tokenized).text_embeds.squeeze(0).detach().numpy().astype('float32')
            text_embeddings.append(embedding)
            id_array.append(int(row['ID']))

        if i % 10 == 0:
            print(f"Processed {i} rows..., end at {df.shape[0]} total rows")
except KeyboardInterrupt:
    print("Interrupted by user. Exiting early.")

    # Convert to arrays
    emb_array = np.stack(text_embeddings)  # shape (n, 768)
    id_array = np.array(id_array, dtype='int64')

    # Save to files
    np.save(os.path.join(save_root, "embeddings.npy"), emb_array)
    np.save(os.path.join(save_root, "ids.npy"), id_array)

    print(f"Saved embeddings: {emb_array.shape}, IDs: {id_array.shape}")
