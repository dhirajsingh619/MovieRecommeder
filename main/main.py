import pickle
import pandas as pd
import streamlit as st
import requests
from PIL import Image
from streamlit_option_menu import option_menu

#@st.cache(allow_output_mutation=True)
selected= option_menu(
    menu_title="MovieForYou.com",
    options=["Home","Top 50"],
    icons=["house","book","trophy"],
    menu_icon="arrow-right",
    default_index=0,
    orientation="horizontal",
)
if selected=="Home":
    st.title(f"{selected}")


    def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        #recommended_movies_poster = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id

            recommended_movies.append(movies.iloc[i[0]].title)
            #recommended_movies_poster.append(fetch_poster(movie_id))
        return recommended_movies#, recommended_movies_poster


    # have to write code again..
    # extra
    def recommends(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        # recommended_movies_poster=[]

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id

            recommended_movies.append(movies.iloc[i[0]].title)
            # recommended_movies_poster.append(fetch_poster(movie_id))
        return recommended_movies  # ,recommended_movies_poster


    # extra

    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)

    similarity = pickle.load(open('similarity.pkl', 'rb'))

#    st.title('MovieForYou')
    # try

    img = Image.open('Images/a2.jpg')
    st.image(img, use_column_width=True)
    # slider
    # x = st.slider('x')
    #n = st.number_input('Number of movie recommendations:', min_value=1, max_value=10, step=1)
    # st.markdown(f'`{x}` squared is `{x * x}`')

    # /try
    selected_movie_name = st.selectbox('We show what you like to see...', movies['title'].values)

    # -->last edit
    #remove1
    if st.button('Recommend'):
        try:
            names = recommends(selected_movie_name)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(names[0])
                img = Image.open('Images/vedio_plar.png')
                st.image(img, use_column_width=True)
                # st.image(poster[0])
            with col2:
                st.text(names[1])
                img = Image.open('Images/vedio_plar.png')
                st.image(img, use_column_width=True)
                # st.image(poster[1])
            with col3:
                st.text(names[2])
                img = Image.open('Images/vedio_plar.png')
                st.image(img, use_column_width=True)
                # st.image(poster[2])
            with col4:
                st.text(names[3])
                img = Image.open('Images/vedio_plar.png')
                st.image(img, use_column_width=True)
                # st.image(poster[3])
            with col5:
                st.text(names[4])
                img = Image.open('Images/vedio_plar.png')
                st.image(img, use_column_width=True)
        except:
            st.text("No information about this Movie")
            st.text('Sorry :(')


if selected=="Top 50":
    st.title(f" {selected} Movies for You")
    Top_50=pickle.load(open('top_50.pkl','rb'))

    st.table(Top_50.iloc[0:50])






