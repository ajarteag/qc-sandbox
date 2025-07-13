# import onnxruntime as ort
from PIL import Image
import numpy as np
# from transformers import CLIPTokenizerFast
# from torchvision import transforms

# import os

# torch_lib_dir = os.path.join(
#     ".venv", "Lib", "site-packages", "torch", "lib"
# )
# torch_lib_dir = os.path.abspath(torch_lib_dir)
# os.add_dll_directory(torch_lib_dir)

import torch

import pandas as pd

from transformers import CLIPTextModel, CLIPTextModelWithProjection, CLIPTokenizer, CLIPVisionModelWithProjection, CLIPVisionModel, AutoProcessor, logging

import torchvision.transforms as T


#I did some reserach? seems like this is the best way to embed images and text with CLIP in Python
#https://colab.research.google.com/github/QUT-GenAI-Lab/genai-explained/blob/main/notebooks/1402%20The%20CLiP%20Text%20Embedding%20Model.ipynb

torch_device = "cpu"

print("Loading CLIP tokenizer...")

tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
text_encoder = CLIPTextModelWithProjection.from_pretrained("openai/clip-vit-large-patch14")

text_encoder = text_encoder.to(torch_device).half()

input_text = "a photo of a black cat"

print("Tokenizing input text...")
tokenized_input = tokenizer(input_text,
    # 'padding' is to fill in "unused" tokens in the input, to make sure it goes into our embedding model properly
    padding="max_length",
    # 'max_length' is setting how many tokens the padder needs to pad the input out to
    max_length=tokenizer.model_max_length,
    # 'truncation' being true means that, if we put in too many tokens, we will just chop off the last tokens to make sure the input fits
    truncation=True,
    # 'return_tensors' set to 'pt' means that our datatype will be compatible with PyTorch
    return_tensors="pt"
)

print("Tokenized input.shape:", tokenized_input.input_ids.shape)
#pprint(tokenized_input) #this is the tokenized input

tokenized_input = tokenized_input.to(torch_device)
sentence_embedding = text_encoder(**tokenized_input)

print("sentence embedding shape:", sentence_embedding.text_embeds.shape) 
#this is the cute little embedding we have 
#print("pooler", sentence_embedding.text_embeds)

print("last hidden state shape:", sentence_embedding.last_hidden_state)

#this is the moral of the story: last hidden state can have varied shapes 
#however the text_embeds and the image_embeds will have the same shape 
#they will both have a shape of (batch_size, 1, 768)
#thus they can be imbedded together in the same space within faiss
#this can also help us to use images to search for the relevant text 
#ultimately the embeddings will be associated with a unique id, calories, sizes in grams, and additional description if we would like 
#we can then pass all of this information to gemma so that it can generate a recommendation 

print("Loading CLIP vision model...")
image_model = CLIPVisionModelWithProjection.from_pretrained("openai/clip-vit-large-patch14")
image_model = image_model.to(torch_device) #move to inference device, halve the precision for better inference speed

processor = AutoProcessor.from_pretrained("openai/clip-vit-large-patch14")

print("Loading image...")
image_location = "./images/donuts.jpg"
input_img = Image.open(image_location).convert("RGB")

print("Loading the processor with the image inputs")
image_inputs = processor(images=input_img, return_tensors="pt")

image_inputs = image_inputs.to(torch_device).to(torch.HalfTensor)

print("Embedding image model")
outputs = image_model(**image_inputs)

print("Image embedding shape:", outputs.image_embeds.shape)





#so now that i have the outputs and everything 
#I want to run faiss on these outputs and add metadata to them so that they can be connected 
# import faiss 


# # 1) Create your base index (e.g. flat inner-product or L2)
# d = 768  # Dimension of the embeddings
# base_index = faiss.IndexFlatIP(d)   # or IndexFlatL2(d)

# # 2) Wrap it so you can add vectors with your own IDs
# index = faiss.IndexIDMap(base_index)


# Detach, move to CPU, convert, and squeeze batch dim:
txt_vec = sentence_embedding.text_embeds.squeeze(0).detach().numpy()   # shape (768,)
img_vec = outputs.image_embeds.squeeze(0).detach().numpy()   # shape (768,)

# 2) Stack into an (n, d) array of float32
emb_array = np.stack([txt_vec, img_vec]).astype('float32')  # shape (2, 768)

# 3) Prepare your IDs as int64
id_array = np.array([100, 200], dtype='int64')               # shape (2,)

root = "./embedding_database/"
np.save(root + "embeddings.npy", emb_array)   # → embeddings.npy
np.save(root + "ids.npy",        id_array)    # → ids.npy

# index.add_with_ids(emb_array, id_array)
# faiss.write_index(index, "faiss_index.faiss")

# # 5) Query later
# query = outputs.image_embeds.detach().numpy()  # shape (1,768)
# D, I = index.search(query, k=5)
# print("Top-5 IDs:", I[0])
# print(D, I)

# 1) Read the index file
# index = faiss.read_index("clip_index.faiss")

#you may periodically write and update faiss but usually you will not need to do it for this project


#interesting issue that cvame up is that multipel copies of openmp runtime have been linked tothe program 
#you cna'ta be having this, so you needed to ensure only 1 is running at at time 

