import pandas as pd
import streamlit as st
import pickle
import pandas
import requests
import datetime

st.set_page_config(page_title='cinema Nexus', layout='wide')

hide_github_icon_js = """
<style>
#MainMenu {
    display: none;
}
[type=button]:not(:disabled), [type=reset]:not(:disabled), [type=submit]:not(:disabled), button:not(:disabled) {
    cursor: default !important;
}
</style>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const githubIcon = document.querySelector('[data-testid="stImageGithubIcon"]');
    if (githubIcon) {
        githubIcon.style.display = 'none';
    }
});
</script>
"""
st.markdown(hide_github_icon_js, unsafe_allow_html=True)




asset_url = 'https://github.com/iamanimesh11/cinema_nexus/releases/download/streamlite/similarity.pkl'
def download_asset(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Download the asset and save it with the desired filename
download_asset(asset_url, 'similarity.pkl')
#   liked........
def log_action(action, timestamp):
    with open("like_log.txt", "a") as log_file:
        log_file.write(f"{action}: {timestamp}\n")
#   liked........
if st.sidebar.button("Liked the page?"):
    
# Process the feedback here

    current_time = datetime.datetime.now()
    log_action("Page Liked", current_time)
    st.success("You liked this page!")
    st.sidebar.success("Liked")


rate_me = st.sidebar.slider("popcorn🍿 digestion?", min_value=1, max_value=5, step=1)
if rate_me:
    current_time = datetime.datetime.now()
    log_action(f"Rated: {rate_me} stars", current_time)
    st.sidebar.write("Thanks :)")

# updates notifications:::



marquee_style = """
<style>
.marquee {
    width: 100%;
    overflow: hidden;
    white-space: nowrap;
}
.marquee p {
    display: inline-block;
    padding-left: 100%;
    animation: marquee 10s linear infinite;
    color: yellow;
}
@keyframes marquee {
    0% { transform: translate(0, 0); }
    100% { transform: translate(-100%, 0); }
}
</style>
"""



marquee_html = '<div class="marquee"><p>updates soon!! &nbsp;&nbsp;&nbsp;</p></div>'
st.markdown(marquee_style, unsafe_allow_html=True)
st.markdown(marquee_html, unsafe_allow_html=True)

def fetch_poster(movie_id):
     response =requests.get('https://api.themoviedb.org/3/movie/{}?api_key=98df14e19b61a51d1c85c25706274353&language=en-US'.format(movie_id))
     data = response.json()

     return  "http://image.tmdb.org/t/p/w500/" +data['poster_path']

movies_list = pickle.load(open('movies.pkl','rb'))
movies_list = pd.DataFrame(movies_list)
similarity = pickle.load(open("similarity.pkl",'rb'))

def recommend(movie):
    index = movies_list[movies_list['title'] ==movie].index[0]
    movie_rec_list =sorted(list(enumerate(similarity[index])),reverse=True, key=lambda x :x[1])

    recommended_movies_list = []
    recommended_movies_list_poster= []
    for i in movie_rec_list[1:7]:
        movie_id = movies_list.iloc[i[0]].movie_id
        #fetch poster from api
        recommended_movies_list.append(movies_list.iloc[i[0]].title)
        recommended_movies_list_poster.append(fetch_poster(movie_id))
    return recommended_movies_list,recommended_movies_list_poster

st.markdown(
    """
    <style>
    .movie-title {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .movie-poster {
        max-width: 200px;
        display: block;
        margin: 0 auto;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }
    .recommendations-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        padding: 20px 0;
    }
    .recommendation-card {
        padding: 10px;
        margin: 10px;
        border: 1px solid #d9d9d9;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        max-width: 220px;
        text-align: center;
    }
    .recommendation-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("About this app")
st.sidebar.write("With a vast database of movies and a powerful recommendation algorithm, Movie Suggest helps you discover your next favorite films effortlessly.")
st.sidebar.write("app generates personalized movie recommendations based on your favorite films. Simply type in the name of a movie you love, and Movie Suggest will present you with a handpicked list of similar movies that are sure to pique your interest.")
st.sidebar.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--Animesh")
st.title("Cinema Nexus..")
st.markdown(
    "Made by Animesh | [Github](https://github.com/iamanimesh11) | [LinkedIn](https://www.linkedin.com/in/animesh-singh11)")

movie_names_options = [''] + movies_list['title'].values.tolist()
movie_name_selections= st.selectbox('Hey there, movie enthusiast! 🍿 Ready to find your favorite movie? ',movie_names_options)
st.text("Try movies : Avatar, Spectre ,Tangled,Interstelllar, Man of steel")


def recommend_more(movie):
    index = movies_list[movies_list['title'] == movie].index[0]
    movie_rec_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommendedmore_movies_list = []
    recommendedmore_movies_list_poster = []
    for i in movie_rec_list[6:12]:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommendedmore_movies_list.append(movies_list.iloc[i[0]].title)
        recommendedmore_movies_list_poster.append(fetch_poster(movie_id))
    return recommendedmore_movies_list, recommendedmore_movies_list_poster

if st.button("Launch Cinema 🎦."):
    if movie_name_selections.strip() == "":
        st.warning('Movies await!🍿 Select one now')
    else:
        recommended_movie_names, recommended_movie_posters = recommend(movie_name_selections)
        num_recommendations = len(recommended_movie_names)



        st.markdown(
            "<div class='recommendations-container'>",
            unsafe_allow_html=True
        )

        for i in range(0, num_recommendations, 3):
            cols = st.columns(3)
            for j in range(min(3, num_recommendations - i)):
                with cols[j]:
                    st.markdown(
                        f"<div class='recommendation-card'>"
                        f"<p class='movie-title'>{recommended_movie_names[i + j]}</p>"
                        f"<img class='movie-poster' src='{recommended_movie_posters[i + j]}' alt='Poster'>"
                        "</div>",
                        unsafe_allow_html=True
                    )

        st.markdown("</div>", unsafe_allow_html=True)


if  st.button("popcorns🍿 left? "):
    if movie_name_selections.strip() == "":
        st.warning('Movies await!🍿 Select one now')
    else:
        recommended_movie_names, recommended_movie_posters = recommend_more(movie_name_selections)
        num_recommendations = len(recommended_movie_names)

        st.markdown(
            "<div class='recommendations-container'>",
            unsafe_allow_html=True
        )

        for i in range(0, num_recommendations, 3):
            cols = st.columns(3)
            for j in range(min(3, num_recommendations - i)):
                with cols[j]:
                    st.markdown(
                        f"<div class='recommendation-card'>"
                        f"<p class='movie-title'>{recommended_movie_names[i + j]}</p>"
                        f"<img class='movie-poster' src='{recommended_movie_posters[i + j]}' alt='Poster'>"
                        "</div>",
                        unsafe_allow_html=True
                    )

        st.markdown("</div>", unsafe_allow_html=True)


