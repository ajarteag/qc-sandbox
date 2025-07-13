import streamlit as st
import subprocess
import os
from PIL import Image, UnidentifiedImageError
import io
import uuid

class AskDanApp:
    def __init__(self):
        self.image_file = None
        self.description = ""
        self.image_path = ""
        if "meals" not in st.session_state:
            st.session_state.meals = []
    
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
                # self.image_path = self.save_temp_image()
                image_bytes = self.image_file.read()
                with st.spinner("Analyzing with AI..."):
                    result = self.caption_image()
                # os.remove(self.image_path)
                st.markdown("### Dan's Insight: ")
                st.text(result)

                # Save to dashboard
                st.session_state.meals.append({
                    "id": str(uuid.uuid4()),
                    "image": image_bytes,
                    "description": self.description,
                    "nutrition": result
                })
    def run_dashboard(self):
        st.title("📋 Meal Dashboard")

        if not st.session_state.meals:
            st.info("No meals submitted yet.")
            return

        for i, meal in enumerate(st.session_state.meals):
            st.subheader(f"🍱 Meal #{i+1}")
            try:
                if os.path.exists(meal["image"]):
                    img = Image.open(meal["image"])
                    st.image(img, use_column_width=True)
                else:
                    st.warning(f"Image not found: {meal['image']}")
            except UnidentifiedImageError:
                st.error(f"Unable to read image: {meal['image']}")

            st.markdown(f"**Description:** {meal['description']}")
            st.markdown("**Nutrition Insight:**")
            st.text(meal["nutrition"])
            st.markdown("---")

        if st.button("Clear All Meals"):
            for meal in st.session_state.meals:
                if os.path.exists(meal["image"]):
                    os.remove(meal["image"])
            st.session_state.meals.clear()
            st.success("All meals cleared.")
    
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
        prompt = f"Analyze this image {self.image_path} of a dish and list each visible ingredient. \
                For each ingredient, estimate the percentage by weight it contributes to the overall dish. \
                Also estimate the total weight of the dish in grams. \
                Present a description of what you see in the image. \
                Present your answer as a list with approximate percentages summing to 100%. \
                Here is also a description of the image to aid with your analysis: {self.description}. "
            
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