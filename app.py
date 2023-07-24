import pandas as pd
import streamlit as st
import pickle
import pandas
import requests
asset_url = 'https://github.com/iamanimesh11/cinema_nexus/releases/download/streamlite/similarity.pkl'
def download_asset(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Download the asset and save it with the desired filename
download_asset(asset_url, 'similarity.pkl')


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
    for i in movie_rec_list[1:6]:
        movie_id = movies_list.iloc[i[0]].movie_id
        #fetch poster from api
        recommended_movies_list.append(movies_list.iloc[i[0]].title)
        recommended_movies_list_poster.append(fetch_poster(movie_id))
    return recommended_movies_list,recommended_movies_list_poster

st.sidebar.title("About this app")
st.sidebar.write("With a vast database of movies and a powerful recommendation algorithm, Movie Suggest helps you discover your next favorite films effortlessly.")
st.sidebar.write("app generates personalized movie recommendations based on your favorite films. Simply type in the name of a movie you love, and Movie Suggest will present you with a handpicked list of similar movies that are sure to pique your interest.")
st.sidebar.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--Animesh")

st.title("Cinema Nexus..")
st.markdown("Made by Animesh | [Github](https://github.com/iamanimesh11) | [LinkedIn](https://www.linkedin.com/in/animesh-singh11)")

movie_names_options = [''] + movies_list['title'].values.tolist()
movie_name_selections= st.selectbox('Hey there, movie enthusiast! 🍿 Ready to find your next favorite film? ',movie_names_options)
st.text("Try movies : Avatar, Spectre ,Tangled,Interstelllar, Man of steel")

#movie_name_selections= st.selectbox('Type the movie name ',movies_list['title'].values)

if st.button("tell me more like this..."):
     if movie_name_selections.strip() == "":
        st.warning('Movies await!🍿 Select one now')
     else:
        recommended_movie_names,recommended_movie_posters= recommend(movie_name_selections)
        num_recommendations = len(recommended_movie_names)
        cols = st.columns(num_recommendations)
        for i, col in enumerate(cols):
            with col:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])


background_image = 'pngwing.com.png'  # Replace with the actual image file name
st.markdown(
    f"""
    <style>
        body {{
            background-image: url("{background_image}");
            background-size: cover;
            background-repeat: no-repeat;
        }}
    </style>
    """,
    unsafe_allow_html=True
)
