import streamlit as st
import sqlite3
import bcrypt
import os
import subprocess
import io
import uuid
import datetime
from PIL import Image

import torch
#import pandas as pd
from transformers import CLIPVisionModelWithProjection, AutoProcessor

import numpy as np
import faiss
import sqlite3

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# ========== USER AUTH ==========
def connect_user_db():
    return sqlite3.connect("users.db")

def create_user_table():
    conn = connect_user_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = connect_user_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        return False
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
    conn.commit()
    conn.close()
    return True

def authenticate_user(username, password):
    conn = connect_user_db()
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return bcrypt.checkpw(password.encode(), result[0]) if result else False

# ========== MEAL DB ==========
def connect_meal_db():
    return sqlite3.connect("meals.db")

def create_meal_table():
    conn = connect_meal_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            meal_name TEXT,
            image BLOB,
            caption TEXT,
            timestamp TEXT,
            nutrition TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_meal(username, meal_name, image_bytes, caption, nutrition):
    conn = connect_meal_db()
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO meals (username, meal_name, image, caption, timestamp, nutrition)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, meal_name, image_bytes, caption, timestamp, nutrition))
    conn.commit()
    conn.close()

def get_user_meals(username):
    conn = connect_meal_db()
    c = conn.cursor()
    c.execute("SELECT meal_name, image, caption, timestamp, nutrition FROM meals WHERE username = ?", (username,))
    rows = c.fetchall()
    conn.close()
    return rows

# ========== APP ==========

class AskDanApp:
    def __init__(self, username):
        self.username = username
        self.image_file = None
        self.description = ""
        self.image_bytes = None

        #backend image model setup 
        self.image_model = CLIPVisionModelWithProjection.from_pretrained("openai/clip-vit-large-patch14")
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
        st.markdown("Upload a photo and add a short food description.")

        self.image_file = st.file_uploader("Upload or take a picture!", type=['png', 'jpg', 'jpeg', 'heic'])
        self.description = st.text_area("Food Description", placeholder="e.g. Toast with eggs and avocado.")

        if self.image_file:
            self.image_bytes = self.image_file.read()
            try:
                image = Image.open(io.BytesIO(self.image_bytes))
                st.image(image, caption="Uploaded Image")
            except Exception as e:
                st.error(f"Image error: {e}")

        if st.button("Submit"):
            if not self.image_bytes or not self.description:
                st.warning("Both image and description are required.")
            else:
                with st.spinner("Analyzing..."):
                    result = self.caption_image()
                st.markdown("### Dan's Insight:")
                st.text(result)

                # Save to database
                add_meal(
                    username=self.username,
                    meal_name=f"Meal {uuid.uuid4().hex[:6]}",
                    image_bytes=self.image_bytes,
                    caption=self.description,
                    nutrition=result
                )
                st.success("Meal saved!")

    #backend process 
    def image_vector(self, img_path):
        print(f"Processing image: {img_path}")
        input_img = Image.open(img_path).convert("RGB")
        image_inputs = self.processor(images=input_img, return_tensors="pt")
        image_inputs = image_inputs.to('cpu').to(torch.HalfTensor)
        outputs = self.image_model(**image_inputs).image_embeds.detach().numpy()
        return outputs
    

    def get_neighbors(self, output_vector, k):
        print(f"Searching for neighbors in FAISS index with k={k}")
        q = output_vector.reshape(1, -1).astype("float32")
        q /= np.linalg.norm(q, axis=1, keepdims=True) + 1e-12
        D, I = self.index.search(q, k)
        return I[0]
    
    def get_db_data(self, neighbors):
        print(f"Fetching data for neighbors: {neighbors}")
        neighbors = [int(n) for n in neighbors]  # Ensure all IDs are valid integers
        conn = sqlite3.connect("./embedding_database/food.db")
        cursor = conn.cursor()

        placeholders = ','.join(['?'] * len(neighbors))

        # Build and execute query
        query = f"SELECT * FROM foods WHERE ID IN ({placeholders})"
        cursor.execute(query, neighbors)

        # Fetch all matching rows
        rows = cursor.fetchall()
        return rows
    

    def process_row(self, rows):
        labeled_rows = []
        for row in rows:
            # Remove ID (row[0])
            name = row[1]
            food_group = row[2]
            calories = f"calories (kcal per 100g): {row[3]}"
            fat = f"fat (g): {row[4]}"
            protein = f"protein (g): {row[5]}"
            carbs = f"carbohydrates (g): {row[6]}"

            # Join all parts with commas
            labeled_row = ", ".join([name, food_group, calories, fat, protein, carbs])
            labeled_rows.append(labeled_row)
        return labeled_rows


    def backend(self, img_path, k=5):  #the goal is to query the database and then provide the 
        #get the image vector 
        output_vector = self.image_vector(img_path)
        #query faiss + get vector id codes 
        neighbors = self.get_neighbors(output_vector, k)
        rows = self.get_db_data(neighbors)
        processed_rows = self.process_row(rows)
        return processed_rows
    
    def caption_image(self):
        image_path = f"temp_{uuid.uuid4().hex}.jpg"
        try:
            with open(image_path, 'wb') as f:
                f.write(self.image_bytes)

            rows = self.backend(image_path, 5)
            rows = "\n".join(rows) if rows else ""

            prompt = (
                f"Analyze this image file: {image_path}. "
                f"Describe what you see and estimate ingredient breakdown. "
                f"User description: {self.description}"
                f"Here are some context with the top entries in the nutrition database for reference for caloric calculations: {rows}"
            )
            print(f"Running Ollama with prompt: {prompt}")
            result = subprocess.run(["ollama", "run", "gemma3:4b", prompt],
                                    capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                return f"Error running Ollama: {result.stderr.strip()}"
            return result.stdout.strip()
        except Exception as e:
            return f"Exception: {e}"
        finally:
            if os.path.exists(image_path):
                os.remove(image_path)

    def run_dashboard(self):
        st.title("📋 Meal Dashboard")
        meals = get_user_meals(self.username)
        if not meals:
            st.info("No meals logged yet.")
            return

        for meal_name, image_blob, caption, timestamp, nutrition in meals:
            st.markdown("----")
            cols = st.columns([1, 2])
            with cols[0]:
                try:
                    st.image(image_blob, caption=meal_name, width=200)
                except Exception as e:
                    st.error(f"Image error: {e}")
            with cols[1]:
                st.markdown(f"**Timestamp:** {timestamp}")
                st.markdown(f"**Description:** {caption}")
                st.markdown(f"**Nutrition Info:** {nutrition}")

# ========== MAIN ==========

def main():
    st.set_page_config(page_title="Ask DAN", page_icon="🥗")
    create_user_table()
    create_meal_table()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if not st.session_state.logged_in:
        auth_menu = st.sidebar.radio("Login/Register", ["Login", "Register"], key="Login/Register")

        if auth_menu == "Register":
            st.subheader("Register")
            new_user = st.text_input("Username")
            new_pass = st.text_input("Password", type='password')
            if st.button("Register"):
                if new_user and new_pass:
                    if add_user(new_user, new_pass):
                        st.success("Registered! Please log in.")
                    else:
                        st.warning("Username already exists.")
                else:
                    st.warning("Fill in all fields.")

        elif auth_menu == "Login":
            st.subheader("Login")
            user = st.text_input("Username")
            pw = st.text_input("Password", type='password')
            if st.button("Login"):
                if authenticate_user(user, pw):
                    st.session_state.logged_in = True
                    st.session_state.username = user
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
    else:
        st.sidebar.markdown(f"👤 Logged in as: **{st.session_state.username}**")
        if st.sidebar.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state["Login/Register"] = "Login"
            st.rerun()

        app = AskDanApp(username=st.session_state.username)
        app.run()

if __name__ == "__main__":
    main()
