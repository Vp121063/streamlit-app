import streamlit as st
import json
import os

# File to store user credentials
USER_CREDENTIALS_FILE = "users.json"

def load_users():
    if os.path.exists(USER_CREDENTIALS_FILE):
        with open(USER_CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USER_CREDENTIALS_FILE, "w") as file:
        json.dump(users, file)

def signup(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists. Please log in."
    users[username] = password
    save_users(users)
    return True, "Signup successful! Please log in."

def login(username, password):
    users = load_users()
    if username in users and users[username] == password:
        return True, "Login successful!"
    return False, "Invalid username or password."

def main():
    st.title("Login System")
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign Up":
        st.subheader("Create a new account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            success, message = signup(new_user, new_password)
            if success:
                st.success(message)
            else:
                st.error(message)
    
    elif choice == "Login":
        st.subheader("Login to your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, message = login(username, password)
            if success:
                st.success(message)
                st.session_state["authenticated"] = True
                
                st.markdown(
                    '<meta http-equiv="refresh" content="1;URL=https://www.vegapay.tech/">',
                    unsafe_allow_html=True,
                )
            else:
                st.error(message)


if __name__ == "__main__":
    main()
