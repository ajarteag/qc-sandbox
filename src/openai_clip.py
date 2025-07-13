import onnxruntime as ort
from PIL import Image
import numpy as np
import torch
from transformers import CLIPTokenizerFast
from torchvision import transforms

# ---- Load ONNX CLIP model ----
session = ort.InferenceSession("./models/openai_clip.onnx", providers=["CPUExecutionProvider"])

# ---- Preprocessing for image ----
image_preprocess = transforms.Compose([
    transforms.Resize(224, interpolation=Image.BICUBIC),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073],
                         std=[0.26862954, 0.26130258, 0.27577711])
])

def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = image_preprocess(image).unsqueeze(0).numpy()
    return image_tensor.astype(np.float32)

# ---- Tokenizer for text ----
tokenizer = CLIPTokenizerFast.from_pretrained("openai/clip-vit-base-patch32") #so we actually cache this locally as well 


def preprocess_text(prompt):
    tokens = tokenizer(prompt, padding="max_length", max_length=77, return_tensors="np")
    return tokens["input_ids"].astype(np.int32)

def normalize(vec):
    return vec / np.linalg.norm(vec, axis=-1, keepdims=True)

# --- Run model and compute similarity ---
def compute_similarity(session, image_tensor, label):
    text_input = preprocess_text(label)  # [1, 77]
    outputs = session.run(None, {
        "image": image_tensor,
        "text": text_input
    })

    # print("these are my outputs ", outputs)
    # image_emb, text_emb = normalize(outputs[0]), normalize(outputs[1])
    # similarity = np.dot(image_emb, text_emb.T)[0][0]
    return outputs[0][0][0]  # Assuming the first output is the similarity score

# --- Main execution ---
image_tensor = preprocess_image("./images/donuts.jpg")

# Your list of text labels
texts = [
    "a photo of a burger with lettuce",
    "a plate of sushi",
    "a bowl of chicken curry",
    "a slice of pepperoni pizza",
    "a photo of green salad",
    "a photo of a donut"
]


# Compute and print similarity for each
print("Similarity scores:")
for label in texts:
    score = compute_similarity(session, image_tensor, label)
    print("The text label '{}' has a similarity score of {:.4f}".format(label, score))