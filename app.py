import streamlit as st
from login_logout import sign_up, sign_in, sign_out
from get_recs import pref_and_recs
from saved_recs import display_saved_recommendations
from database import init_db

# Initialize the database (ensures tables exist)
init_db()

# Set page configuration with an emoji favicon and title
st.set_page_config(
    page_title="Popcorn Picks",
    page_icon="🍿",  # Emoji for the favicon
    layout="centered",  # Center content on the page
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #7B68EE; /* Purple background */
            color: white; /* White text */
        }
        .stButton>button {
            background-color: #4B0082; /* Indigo button */
            color: white; /* White text on buttons */
        }
        .stButton>button:hover {
            background-color: #6A0DAD; /* Hover effect */
            color: white;
        }
        .stSidebar {
            background-color: #4B0082 !important; /* Purple sidebar */
        }
        .sidebar-content {
            color: white !important; /* White text in sidebar */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session states if not already initialized
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False  # Tracks if user is logged in
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None  # Stores the username of the logged-in user

# Streamlit Sidebar for Navigation
st.sidebar.title("🍿 Navigation")

# Check if the user is logged in
if not st.session_state["logged_in"]:
    # Show only Sign Up and Sign In options if not logged in
    page = st.sidebar.radio("Select a page", ["🔑 Sign Up", "🔓 Sign In"])
else:
    # Show Home and Saved Recommendations when logged in
    page = st.sidebar.radio("Select a page", ["🏠 Home", "📚 Saved Recommendations"])

# Show different content based on selected page
if page == "🏠 Home":
    if st.session_state["logged_in"]:
        st.title(f"Welcome, {st.session_state['current_user']}! 🎥")
        pref_and_recs()  # Movie recommendations page
    else:
        st.warning("You need to sign in or sign up to access the Home page. 🚪")

elif page == "🔑 Sign Up":
    sign_up()

elif page == "🔓 Sign In":
    sign_in()

elif page == "📚 Saved Recommendations":
    if st.session_state["logged_in"]:
        display_saved_recommendations()  # Display the saved recommendations
    else:
        st.warning("You need to sign in to view your saved recommendations. 🔒")

# Sign-out button visible in the sidebar when logged in
if st.session_state["logged_in"]:
    st.sidebar.button("🚪 Sign Out", on_click=sign_out)
