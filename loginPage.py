import streamlit as st
import psycopg2
import os

# PostgreSQL Connection
DB_HOST = "localhost"
DB_NAME = "aihackathon"
DB_USER = "postgres"
DB_PASS = "postgres"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# Create user table if not exists
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def signup(first_name, last_name, email, username, password):
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if user exists
    cur.execute("SELECT * FROM users WHERE email=%s OR username=%s", (email, username))
    if cur.fetchone():
        cur.close()
        conn.close()
        return False, "Email or Username already exists. Please log in."

    # Insert new user
    cur.execute(
        "INSERT INTO users (first_name, last_name, email, username, password) VALUES (%s, %s, %s, %s, %s)",
        (first_name, last_name, email, username, password)
    )
    conn.commit()
    cur.close()
    conn.close()
    return True, "Signup successful! Please log in."

def login(email_or_username, password):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=%s OR username=%s", (email_or_username, email_or_username))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user and user[5] == password:  # user[5] is the password column
        return True, "Login successful!"
    return False, "Invalid username/email or password."

def main():
    st.title("Login System with PostgreSQL")
    create_table()  # Ensure table is created

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign Up":
        st.subheader("Create a new account")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign Up"):
            success, message = signup(first_name, last_name, email, username, password)
            if success:
                st.success(message)
            else:
                st.error(message)

    elif choice == "Login":
        st.subheader("Login to your account")
        email_or_username = st.text_input("Email / Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            success, message = login(email_or_username, password)
            if success:
                st.success(message)

                # ✅ Redirect to Vegapay website after login
                st.markdown(
                    '<meta http-equiv="refresh" content="1;URL=https://www.vegapay.tech/">',
                    unsafe_allow_html=True,
                )
            else:
                st.error(message)

if __name__ == "__main__":
    main()
    
