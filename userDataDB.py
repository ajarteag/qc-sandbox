import streamlit as st
import sqlite3
import datetime

def connect_db():
    return sqlite3.connect("meals.db")

def create_meal_table():
    conn = connect_db()
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

def add_meal(username, meal_name, image_file, caption, nutrition):
    conn = connect_db()
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_blob = image_file.read() if image_file else None
    c.execute('''
        INSERT INTO meals (username, meal_name, image, caption, timestamp, nutrition)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, meal_name, image_blob, caption, timestamp, nutrition))
    conn.commit()
    conn.close()

def get_user_meals(username):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT meal_name, image, caption, timestamp, nutrition FROM meals WHERE username = ?", (username,))
    rows = c.fetchall()
    conn.close()
    return rows

# ---------- STREAMLIT INTERFACE ---------- #

def main():
    st.title("🍽️ Meal Logger")

    username = st.text_input("Enter your username")

    if username:
        create_meal_table()

        menu = ["Add Meal", "View Meals"]
        choice = st.sidebar.radio("Menu", menu)

        if choice == "Add Meal":
            st.subheader("📸 Log a New Meal")
            meal_name = st.text_input("Meal Name")
            image_file = st.file_uploader("Upload Meal Image", type=["jpg", "png", "jpeg"])
            caption = st.text_area("Meal Caption")
            nutrition = st.text_area("Nutrition Info (e.g., 500 kcal, 20g protein)")

            if st.button("Save Meal"):
                if meal_name:
                    add_meal(username, meal_name, image_file, caption, nutrition)
                    st.success("Meal saved successfully!")
                else:
                    st.warning("Meal name is required.")

        elif choice == "View Meals":
            st.subheader(f"📚 Meals for: {username}")
            meals = get_user_meals(username)
            if meals:
                for meal_name, image, caption, timestamp, nutrition in meals:
                    st.markdown(f"### {meal_name} ({timestamp})")
                    if image:
                        st.image(image, width=300)
                    st.write(f"📝 {caption}")
                    st.write(f"💪 Nutrition: {nutrition}")
                    st.markdown("---")
            else:
                st.info("No meals logged yet.")

if __name__ == "__main__":
    main()