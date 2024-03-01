%load_ext autoreload
%autoreload 2

import pandas as pd
import numpy as mp
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from wordcloud import WordCloud
from PIL import Image  # pillow == 9.5

# load `new_orleans_reviews` dataset
new_orleans_reviews = pd.read_csv('notebooks/csv/df_review_top10.csv')

# load `new_orleans_restaurants` dataset
new_orleans_business = pd.read_csv('notebooks/csv/df_business_top10.csv')

new_orleans_restaurants = new_orleans_business[new_orleans_business['categories'].str.contains('restaurant', case=False, na=False)]

sample_restaurant = new_orleans_restaurants[new_orleans_restaurants['name'] == "Mother's Restaurant"]

def res_in_same_cat(res_name:str) -> pd.DataFrame:
    """
    Get dataframe of other restaurants in same category, excluding user's restaurant
    First category from categories is picked.
    If first category is "Restaurants", second category will be used.
    
    """
    categories = new_orleans_restaurants.loc[new_orleans_restaurants['name'] == res_name]['categories']
    
    # convert series to string and split string to access first label (assumption)
    cat = categories.to_list()[0].split(", ")[0]
    print(cat)
    if cat == 'Restaurants':
        cat = categories.to_list()[0].split(", ")[1]
        print(cat)
    
    return new_orleans_restaurants.loc[(new_orleans_restaurants['categories'].str.contains(cat, case=False))
                                                 & (new_orleans_restaurants['name'] != res_name)]

# test function with our sample restaurant
same_cat_restaurants = res_in_same_cat("Mother's Restaurant")

# merge `reviews` with `same_cat_business` on business_id
same_cat_reviews = pd.merge(new_orleans_reviews, same_cat_restaurants, on='business_id')

