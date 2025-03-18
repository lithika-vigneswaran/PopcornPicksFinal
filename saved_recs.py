import streamlit as st
from database import get_user_recommendations

def display_saved_recommendations():
    """Display the user's saved movie recommendations."""
    username = st.session_state["current_user"]

    if username:
        recommendations = get_user_recommendations(username)

        if recommendations:
            st.subheader("Your Saved Movie Recommendations:")
            for movie in recommendations:
                st.write(f"**Title**: {movie[0]}")
                st.write(f"**Release Date**: {movie[1]}")
                st.write(f"**Synopsis**: {movie[2]}")
                st.write("--------")
        else:
            st.info("You haven't saved any movie recommendations yet.")
    else:
        st.warning("Please log in to view your saved recommendations.")
