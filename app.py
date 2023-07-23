import pandas as pd
import streamlit as st
import pickle
import pandas
import requests

def download_similarity_file(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, "wb") as f:
            f.write(response.content)
    else:
        st.error("Error downloading the similarity file.")

# Replace "YOUR_FILE_ID" with the actual File ID of your similarity.pkl file on Google Drive
similarity_file_id = "1ZBUzHW5-knm-lo2AMiFVopnzKXwCZorx"
similarity_file_path = "similarity.pkl"
download_similarity_file(similarity_file_id, similarity_file_path)
def fetch_poster(movie_id):
     response =requests.get('https://api.themoviedb.org/3/movie/{}?api_key=98df14e19b61a51d1c85c25706274353&language=en-US'.format(movie_id))
     data = response.json()

     return  "http://image.tmdb.org/t/p/w500/" +data['poster_path']

movies_list = pickle.load(open('movies.pkl','rb'))
movies_list = pd.DataFrame(movies_list)
similarity = pickle.load(open(similarity_file_path,'rb'))

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


st.title("Movie recommender System")
movie_names_options = [''] + movies_list['title'].values.tolist()
movie_name_selections= st.selectbox('Type the movie name ',movie_names_options)
#movie_name_selections= st.selectbox('Type the movie name ',movies_list['title'].values)

if st.button("tell me more like this..."):
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