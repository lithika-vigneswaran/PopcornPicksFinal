import requests
import sqlite3
import streamlit as st
from database import save_recommendation

# # SAVING MOVIE RECOMMENDATIONS
def save_stuff(person, title, day, overview):
    save_recommendation(title, day, overview, person)
    print(f"Recommendation saved: {(person, title, day, overview)}")

# # END OF SAVING MOVIE RECOMMENDATIONS

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

    # Step 3a: Initialize Movies
    movies = []

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
            else:
                st.error("Failed to fetch movie recommendations. Please try again later.")
    # End of Get your picks!!!
    
    # Step 4: The Button fetched the movies, now to save movies!
    if movies:
        st.subheader("🎥 Recommended Movies:")
                    
        for movie in movies[:10]:
            col1, col2 = st.columns([1, 4])
            poster_path = movie["poster_path"]
            movie_title = movie.get('title', 'Title not found!')

            with col1:
                if poster_path:
                    poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                    st.image(poster_url, width=120, caption=movie['title'])
                else:
                    st.write("No Poster Available")

            with col2:
                st.write(f"**Title**: {movie_title}")
                st.write(f"**Release Date**: {movie.get('release_date', 'N/A')}")
                st.write(f"**Synopsis**: {movie.get('overview', 'No synopsis available.')}")

                current_person = st.session_state["current_user"]

                if st.button(f"Save '{movie['title']}'", key=f"save-{movie['id']}", on_click=save_stuff, args=[current_person, movie['title'], movie.get('release_date', 'N/A'), movie.get('overview', 'No synopsis available.')]):
                    pass
                
                st.write("--------")
    else:
        st.info("No movies found matching your preferences.")
                