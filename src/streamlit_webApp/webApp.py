import streamlit as st
import subprocess
import os
from PIL import Image
import io
import uuid

class AskDanApp:
    def __init__(self):
        self.image_file = None
        self.description = ""
        self.image_bytes = None  # Store raw bytes here
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

    def caption_image(self):
        # Save image to a temp file for analysis
        image_path = f"temp_{uuid.uuid4().hex}.jpg"
        try:
            with open(image_path, 'wb') as f:
                f.write(self.image_bytes)

            # Create prompt
            prompt = (
                f"Analyze this image file: {image_path}. "
                f"List all visible ingredients. Estimate the percentage by weight for each ingredient. "
                f"Estimate total dish weight in grams. Describe what you see. Percentages should sum to ~100%. "
                f"Here is a user-provided description: {self.description}"
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
