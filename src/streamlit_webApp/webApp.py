import streamlit as st
import subprocess
import os
from PIL import Image
import io
import uuid

import torch
import pandas as pd
from transformers import CLIPTextModel, CLIPTextModelWithProjection, CLIPTokenizer, CLIPVisionModelWithProjection, CLIPVisionModel, AutoProcessor, logging
import torchvision.transforms as T
import numpy as np
import faiss
import sqlite3


class AskDanApp:
    def __init__(self):
        self.image_file = None
        self.description = ""
        self.image_bytes = None  # Store raw bytes here
        if "meals" not in st.session_state:
            st.session_state.meals = []

        #backend image model setup 
        self.image_model = CLIPVisionModelWithProjection.from_pretrained("openai/clip-vit-large-patch14")
        self.image_model = self.image_model.to('cpu')
        self.processor = AutoProcessor.from_pretrained("openai/clip-vit-large-patch14")
        self.index = faiss.read_index("./embedding_database/faiss_index.faiss")

    def run(self):
        st.sidebar.title("🍽️ Navigation")
        page = st.sidebar.radio("Go to", ["Home", "Meal Dashboard"])

        if page == "Home":
            self.run_home()
        elif page == "Meal Dashboard":
            self.run_dashboard()

    def run_home(self):
        st.title("Ask DAN: Your Daily Assistant for Nutrition")
        st.markdown(
            "Take a picture of your food and write a short description "
            "for a detailed calorie / nutrient breakdown."
        )

        self.image_file = st.file_uploader("Upload or take a picture of your food!", type=['png', 'jpg', 'jpeg', 'heic'])

        self.description = st.text_area(
            "Food Description",
            placeholder="e.g. Two scrambled eggs with toast and orange juice for my breakfast."
        )

        if self.image_file is not None:
            self.image_bytes = self.image_file.read()
            try:
                image = Image.open(io.BytesIO(self.image_bytes))
                st.image(image, caption="Uploaded Image")
            except Exception as e:
                st.error(f"Error displaying image: {e}")

        if st.button("Submit"):
            if not self.image_bytes or not self.description:
                st.warning("Please upload an image and enter a description before submitting.")
            else:
                with st.spinner("Analyzing with AI..."):
                    result = self.caption_image()
                st.markdown("### Dan's Insight:")
                st.text(result)

                # Save to dashboard
                st.session_state.meals.append({
                    "id": str(uuid.uuid4()),
                    "image": self.image_bytes,
                    "description": self.description,
                    # "nutrition": result
                })

    def run_dashboard(self):
        st.title("📋 Meal Dashboard")

        if not st.session_state.meals:
            st.info("No meals submitted to the dashboard yet.")
            return

        for i, meal in enumerate(st.session_state.meals):
            with st.container():
                st.markdown("----")
                cols = st.columns([1,2])

                #Left: smaller image
                with cols[0]:
                    try:
                        img = Image.open(io.BytesIO(meal["image"]))
                        st.image(img, caption=f"Meal #{i+1}", width=200)
                    except Exception as e:
                        st.error(f"Unable to load image: {e}")
                #Right: description and nutrition
                with cols[1]:
                    st.markdown(f"**Your Description:** {meal['description']}")
                    # st.markdown("**Dan's Nutrition Insight:**")
                    # st.text(meal["nutrition"])

        st.markdown("---")
        if st.button("Clear All Meals"):
            st.session_state.meals.clear()
            st.success("All meals cleared.")


    #backend process 
    def image_vector(self, img_path):
        input_img = Image.open(img_path).convert("RGB")
        image_inputs = self.processor(images=input_img, return_tensors="pt")
        image_inputs = image_inputs.to('cpu').to(torch.HalfTensor)
        outputs = self.image_model(**image_inputs).image_embeds.detach().numpy()
        return outputs
    

    def get_neighbors(self, output_vector, k):
        q = output_vector.reshape(1, -1).astype("float32")
        q /= np.linalg.norm(q, axis=1, keepdims=True) + 1e-12
        D, I = self.index.search(q, k)
        return I[0]
    
    def get_db_data(self, neighbors):
        conn = sqlite3.connect("./embedding_database/food.db")
        cursor = conn.cursor()

        placeholders = ','.join(['?'] * len(neighbors))

        # Build and execute query
        query = f"SELECT * FROM foods WHERE ID IN ({placeholders})"
        cursor.execute(query, neighbors)

        # Fetch all matching rows
        rows = cursor.fetchall()
        return rows


    def backend(self, img_path, k=5):  #the goal is to query the database and then provide the 
        #get the image vector 
        output_vector = self.image_vector(img_path)

        #query faiss + get vector id codes 
        neighbors = self.get_neighbors(output_vector, k)

        rows = self.get_db_data(neighbors)

        return rows


        
    def caption_image(self):
        # Save image to a temp file for analysis
        image_path = f"temp_{uuid.uuid4().hex}.jpg"
        try:
            with open(image_path, 'wb') as f:
                f.write(self.image_bytes)

            rows = self.backend(image_path, 5)
            print(rows)

            # Create prompt
            prompt = (
                f"Analyze this image file: {image_path}. "
                f"List all visible ingredients. Estimate the percentage by weight for each ingredient. "
                f"Estimate total dish weight in grams. Describe what you see. Percentages should sum to ~100%. "
                f"Here is a user-provided description: {self.description}"
                f"Here are some context for your understanding: {rows}"
            )

            # Call Ollama CLI with prompt
            result = subprocess.run(
                ["ollama", "run", "gemma3:4b", prompt],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            if result.returncode != 0:
                return f"Error running Ollama: {result.stderr.strip()}"

            return result.stdout.strip()

        except Exception as e:
            return f"Exception occurred: {e}"
        finally:
            if os.path.exists(image_path):
                os.remove(image_path)


if __name__ == "__main__":
    app = AskDanApp()
    app.run()
