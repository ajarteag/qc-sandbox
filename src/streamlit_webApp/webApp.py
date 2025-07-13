import streamlit as st
import subprocess
import os
from PIL import Image

class AskDanApp:
    def __init__(self):
        self.image_file = None
        self.description = ""
        self.image_path = ""
    
    def run(self):
        st.title("Ask DAN: Your Daily Assistant for Nutrition")
        st.markdown(
            "Take a picture of your food and write a short description "
            "for a detailed calorie / nutrient breakdown.")
        
        self.image_file = st.file_uploader("Upload or take a picture of your food!", type=['png', 'jpg', 'jpeg', 'heic'])

        self.description = st.text_area(
            "Food Description",
            placeholder="e.g. Two scrambled eggs with toast and orange juice for my breakfast."
        )

        if self.image_file is not None:
            image = Image.open(self.image_file)
            st.image(image, caption="Uploaded Image")
        
        if st.button("Submit"):
            if not self.image_file or not self.description:
                st.warning("Please upload an image and enter a description before submitting.")
            else:
                self.image_path = self.save_temp_image()
                with st.spinner("Analyzing with AI..."):
                    result = self.caption_image()
                os.remove(self.image_path)
                st.markdown("### Dan's Insight: ")
                st.text(result)
    
    def save_temp_image(self):
        path = f"temp_{self.image_file.name}"
        with open(path, 'wb') as f:
            f.write(self.image_file.read())
        return path

    '''
    Ollama Interface
    '''
    def caption_image(self):
        # Create prompt to send to Ollama
        prompt = f"Analyze this image of a dish and list each visible ingredient. \
                For each ingredient, estimate the percentage by weight it contributes to the overall dish. \
                Also estimate the total weight of the dish in grams. \
                Present your answer as a list with approximate percentages summing to 100%. \
                Here is also a description of the image: {self.description}. \
                {self.image_path}"
            
        # Call ollama
        try:
            result = subprocess.run(
                ["ollama", "run", "gemma3:4b", prompt],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                return f"Error running Ollama: {result.stderr}"
            
            return result.stdout.strip()
        
        except Exception as e:
            return f"Exception occurred: {e}"

if __name__ == "__main__":
    app = AskDanApp()
    app.run()