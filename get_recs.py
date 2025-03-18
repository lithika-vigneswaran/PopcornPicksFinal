import requests
import sqlite3
import streamlit as st
from database import save_recommendation

def save_stuff():
    pass

def pref_and_recs():
    # TMDB API key and API URL
    API_KEY = "2869065f289c63f7b89ae7a41c8cc4cf"
    API_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

    # Fetch genres from TMDB
    url = f"{API_URL}/genre/movie/list"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        genres_data = response.json().get("genres", [])
        genres = {genre["name"]: genre["id"] for genre in genres_data}
    else:
        st.error("Failed to fetch genres. Check your API key.")
        genres = {}

    # Streamlit UI
    st.title("🎬 Movie Recommendation System")

    # Step 1: User selects genre preferences
    selected_genres = st.multiselect(
        "Select your preferred genres:",
        options=list(genres.keys())
    )

    # Step 2: User selects movie mood
    mood = st.radio(
        "Select your preferred Movie Mood:",
        options=["Light-hearted", "Romantic", "Silly", "Sad", "Thrilling"]
    )

    # Step 3: Button for fetching recommendations
    if st.button("Get Your Picks!!"):
        if not selected_genres:
            st.warning("Please select at least one genre!")
        else:
            genre_ids = ",".join(str(genres[genre]) for genre in selected_genres)

            mood_to_keyword_query = {
                "😄 Light-hearted": "comedy",
                "❤️ Romantic": "romance",
                "🤪 Silly": "funny",
                "😭 Sad": "drama",
                "🫨 Thrilling": "thriller"
            }

            keyword_id = None
            if mood in mood_to_keyword_query:
                keyword_search_url = f"{API_URL}/search/keyword"
                params_keyword = {"api_key": API_KEY, "query": mood_to_keyword_query[mood]}
                keyword_response = requests.get(keyword_search_url, params=params_keyword)

                if keyword_response.status_code == 200:
                    keyword_results = keyword_response.json().get("results", [])
                    if keyword_results:
                        keyword_id = keyword_results[0]["id"]

            params = {
                "api_key": API_KEY,
                "language": "en-US",
                "with_genres": genre_ids,
                "sort_by": "popularity.desc",
            }

            if keyword_id:
                params["with_keywords"] = keyword_id

            discover_url = f"{API_URL}/discover/movie"
            response = requests.get(discover_url, params=params)

            if response.status_code == 200:
                movies = response.json().get("results", [])
                if movies:
                    st.subheader("🎥 Recommended Movies:")
                    for movie in movies[:10]:
                        col1, col2 = st.columns([1, 4])

                        with col1:
                            poster_path = movie.get("poster_path")
                            if poster_path:
                                poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                                st.image(poster_url, width=120, caption=movie['title'])
                            else:
                                st.write("No Poster Available")

                        with col2:
                            st.write(f"**Title**: {movie['title']}")
                            st.write(f"**Release Date**: {movie.get('release_date', 'N/A')}")
                            st.write(f"**Synopsis**: {movie.get('overview', 'No synopsis available.')}")
                            print(st.session_state["current_user"])

                            # Save movie to the database for the current user
                            if st.button(f"Save '{movie['title']}'", key=f"save-{movie['id']}"):
                                username = st.session_state["current_user"]
                                print(username)
                                if username:
                                    save_recommendation(username, movie['title'], movie.get('release_date', 'N/A'), movie.get('overview', 'No synopsis available.'))
                                    st.success(f"'{movie['title']}' has been saved to your recommendations!")
                           
                            st.write("--------")
                else:
                    st.info("No movies found matching your preferences.")
            else:
                st.error("Failed to fetch movie recommendations. Please try again later.")
