import pandas as pd
import numpy as  np
import ast
import nltk
import sklearn
import pickle

#read csv file
#data=pd.read_csv('E:\Downloads\cars.csv')
movies=pd.read_csv(r'E:\Downloads\tmdb_5000_movies.csv') #r stands for “raw” and will cause backslashes in the string to be interpreted as actual backslashes rather than special characters.
credits=pd.read_csv(r'E:\Downloads\tmdb_5000_credits.csv')

top_50=pd.read_csv(r'E:\Downloads\IMDB Top 50.csv',encoding='latin-1')
top_50=top_50[['Rank','Title','Rating']]
print(top_50.tail())

#print("step 2")
#print(movies.head(1))
#print(credits.head(1)['crew'].values)
movies=movies.merge(credits,on='title')
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]
#print(movies.shape)

#data preprocessing
#data taken for considersation: genres,id,keywords,tittle,overview,cast ,crew

#print("step 3")

#print(movies.isnull().sum())
movies.dropna(inplace=True)
#print(movies.isnull().sum())
#print(movies.duplicated().sum())

#print(movies.iloc[0].genres)
def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
#preprocessed generes
movies['genres']=(movies['genres'].apply(convert))
#preprocessed keywords
movies['keywords']=movies['keywords'].apply(convert)

def converter(obj):
    L=[]
    count=0
    for i in ast.literal_eval(obj):
        if count!=3:
            L.append(i['name'])
            count+=1
        else:
            break
    return L
#preprocessed cast section
movies['cast']=movies['cast'].apply(converter)


def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
            break
    return L
#preprocessed crew section
movies['crew']=movies['crew'].apply(fetch_director)


#print(movies['overview'][0])
#converting overview to list

movies['overview']=movies['overview'].apply(lambda x:x.split())

#print(movies.head())

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

#concatinatind all the columns

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']
new_df=movies[['movie_id','title','tags']]

# default='warn'(imp)
pd.options.mode.chained_assignment = None

new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))

#print("step 4")
#print(new_df['tags'][0])
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())
#print(new_df.head())


#making vectors

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')

cv.fit_transform(new_df['tags']).toarray()
vectors=cv.fit_transform(new_df['tags']).toarray()
#print('step 5')

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)
new_df['tags']=new_df['tags'].apply(stem)
#print('step 6')

#we will be using cosine of vectors as euclidian distance is not prefered in case of  higher dimension

from sklearn.metrics.pairwise import cosine_similarity
#print(cv.get_feature_names())
similarity=cosine_similarity(vectors)

def recommand(movie):
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:
        print(new_df.iloc[i[0]].title)

#recommand('Avatar')
#export movie
pickle.dump(top_50,open('top50.pkl','wb'))
pickle.dump(new_df,open('movies.pkl','wb'))
pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))