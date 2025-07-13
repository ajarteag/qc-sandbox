import streamlit as st
import sqlite3
import bcrypt

# ---- DATABASE SETUP ----
def connect_db():
    return sqlite3.connect("users.db")

def create_user_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = connect_db()
    c = conn.cursor()

    # Check if username already exists
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = c.fetchone()

    if existing_user:
        conn.close()
        return False  # User already exists

    # Hash the password and insert new user
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
    conn.commit()
    conn.close()
    return True  # User added successfully

def authenticate_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result:
        stored_pw = result[0]
        return bcrypt.checkpw(password.encode(), stored_pw)
    return False

# ---- STREAMLIT APP ----
def main():
    st.title("User Login System")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    create_user_table()


    if choice == "Register":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type='password')

        if st.button("Register"):
            if new_user and new_pass:
                added_successfully = add_user(new_user, new_pass)
                if added_successfully:
                    st.success("User registered successfully!")
                else:
                    st.warning("Username already exists. Please choose a different one.")
            else:
                st.warning("Please fill in both fields.")


    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if authenticate_user(username, password):
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")

if __name__ == "__main__":
    main()