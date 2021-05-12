import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from surprise import Reader
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import SVD, SlopeOne, NMF
from surprise.accuracy import rmse
from surprise import accuracy
from surprise.model_selection import train_test_split

df = pd.read_csv('../data/rating.csv')
anime = pd.read_csv('../data/anime.csv')

df = pd.merge(df,anime.drop('rating',axis=1),on='anime_id')

ratings = pd.DataFrame(df.groupby('name')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('name')['rating'].count())

genre_dict = pd.DataFrame(data=anime[['name','genre']])
genre_dict.set_index('name',inplace=True)

def check_genre(genre_list,string):
    if any(x in string for x in genre_list):
        return True
    else:
        return False
    
def get_recommendation(name):
    #generating list of anime with the same genre with target
    anime_genre = genre_dict.loc[name].values[0].split(', ')
    cols = anime[anime['genre'].apply(
        lambda x: check_genre(anime_genre,str(x)))]['name'].tolist()
    
    #create matrix based on generated list
    animemat = df[df['name'].isin(cols)].pivot_table(
        index='user_id',columns='name',values='rating')
       
    #create correlation table
    anime_user_rating = animemat[name]
    similiar_anime = animemat.corrwith(anime_user_rating)
    corr_anime = pd.DataFrame(similiar_anime,columns=['correlation'])
    corr_anime = corr_anime.join(ratings['num of ratings'])
    corr_anime.dropna(inplace=True)
    corr_anime = corr_anime[corr_anime['num of ratings']>5000].sort_values(
        'correlation',ascending=False)
    
    return corr_anime.head(10)

runnning = True

while(runnning):
    print('What is your favorite anime?')
    x=input()
    try:
        temp = get_recommendation(x)
        print('Based on your favorite anime, we recommend the followin: ')
        print(temp)
    except:
        print('The anime your picked does not exist in our database.')
    print('Would you like to pick again? (Y/y or N/n)')
    x=input()
    if(x == 'N' or x == 'n'):
        runnning = False

print('Thanks! Come again!')
