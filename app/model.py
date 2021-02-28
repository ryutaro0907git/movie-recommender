import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns



class MyRecommender(object):
    def __init__(self):
        self.movies = pd.read_csv("movie-recommender/app/data/movies.csv")
        self.ratings = pd.read_csv("movie-recommender/app/data/ratings.csv")

        self.dataset = self.ratings.pivot(index='movieId',columns='userId',values='rating')
        self.dataset.fillna(0, inplace=True)
        
        self.no_user_voted = self.ratings.groupby('movieId')['rating'].agg('count')
        self.no_movies_voted = self.ratings.groupby('userId')['rating'].agg('count')
        
        self.final_dataset= self.dataset.loc[:,self.no_movies_voted[self.no_movies_voted > 50].index]
        self.csr_matrix_data = csr_matrix(self.final_dataset.values)
        self.final_dataset.reset_index(inplace=True)

        self.model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
        self.model.fit(self.csr_matrix_data)
        
    def recommende_movies(self, movie_name:str):
        movie_name = str(movie_name.title())
        
        n_movies_to_reccomend = 10
        movie_list = self.movies[self.movies['title'].str.contains(movie_name)]  
        if len(movie_list):       
            movie_idx= movie_list.iloc[0]['movieId']
            movie_idx = self.final_dataset[self.final_dataset['movieId'] == movie_idx].index[0]
            distances , indices = self.model.kneighbors(self.csr_matrix_data[movie_idx], n_neighbors=n_movies_to_reccomend+1)    
            rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
            recommend_frame = []
            
            for val in rec_movie_indices:
                movie_idx = self.final_dataset.iloc[val[0]]['movieId']
                idx = self.movies[self.movies['movieId'] == movie_idx].index
                recommend_frame.append(self.movies.iloc[idx]['title'].values[0])
                
            return recommend_frame
        
        else:
            return "No movies found. Please check your input"