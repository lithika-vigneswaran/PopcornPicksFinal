import sqlite3
import streamlit as st
from database import user_exists, authenticate_user, add_user

def sign_up():
    st.title("Sign Up")
    st.write("Create Your Popcorn Picks Account")

    new_username = st.text_input("Enter a username", key="new_username")
    new_password = st.text_input("Enter a password", type="password", key="new_password")
    confirm_password = st.text_input("Confirm your password", type="password", key="confirm_password")
    
    register_button = st.button("Sign Up")

    if register_button:
        if not new_username or not new_password:
            st.error("Username and password cannot be empty.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif user_exists(new_username):
            st.error("Username already exists.")
        else:
            add_user(new_username, new_password)  # Using add_user from the updated database
            st.success("Account created! Please sign in.")

def sign_in():
    st.title("Sign In")
    st.write("Sign in with your username and password")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Sign In")

    if login_button:
        if authenticate_user(username, password):  # Using authenticate_user from the updated database
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = username
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password.")
        
def sign_out():
    st.session_state["logged_in"] = False
    st.session_state["current_user"] = None
    st.success("You have been logged out.")
