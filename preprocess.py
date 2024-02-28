import pandas as pd
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st

# Combine Review and Business Tables
#-----------------------------------
df_review = pd.read_csv('csv/new_orleans_reviews.csv')
df_business = pd.read_csv('csv/yelp_business.csv')
df_combined = pd.merge(df_review, df_business, on='business_id', how='inner')

# Remove the columns
#-----------------------------------
df = df_combined[['review_id', 'user_id', 'business_id', 'stars_x', 'useful','funny','cool','text','date','name','categories']]
df = df.rename(columns={'stars_x': 'stars'})

# Preprocess - Clean Text
#-----------------------------------
def remove_punctuation(text):
    return "".join(char for char in text if not char in string.punctuation)
preprocessed_stopwords= [remove_punctuation(word) for word in stopwords.words('english')]
def preprocessing(sentence):
    # remove whitespace
    t1 = sentence.strip()
    # lowercase characters
    t2 = t1.lower()
    # remove numbers
    t3 = ''.join(char for char in t2 if not char.isdigit())
    # remove punctuation
    t4 = "".join(char for char in t3 if not char in string.punctuation)
    # tokenize
    tokens = t4.split(" ")
    # lemmatize
    stopwords_removed = [
        word for word in tokens if word not in preprocessed_stopwords
    ]
    return " ".join(stopwords_removed)
# Clean reviews
df['clean_text'] = df['text'].apply(preprocessing)

# Pick Top 10 Restaurants and Export to CSV
#-----------------------------------
review_counts = df['business_id'].value_counts().reset_index(name='review_count')
review_counts.columns = ['business_id', 'review_count']

top_10_business_ids = review_counts.head(10)['business_id']
top_10_reviews = df[df['business_id'].isin(top_10_business_ids)]
top_10_reviews.to_csv('csv/df_top10.csv', index=False)


# Pick Top 5 Restaurants and Export to CSV
#-----------------------------------
review_counts = df['business_id'].value_counts().reset_index(name='review_count')
review_counts.columns = ['business_id', 'review_count']
top_5_business_ids = review_counts.head(5)['business_id']
top_5_reviews = df[df['business_id'].isin(top_5_business_ids)]
top_5_reviews.to_csv('csv/df_top5.csv', index=False)

# Pick Top 3 Restaurants and Export to CSV
#-----------------------------------
review_counts = df['business_id'].value_counts().reset_index(name='review_count')
review_counts.columns = ['business_id', 'review_count']
top_3_business_ids = review_counts.head(3)['business_id']
top_3_reviews = df[df['business_id'].isin(top_3_business_ids)]
top_3_reviews.to_csv('csv/df_top3.csv', index=False)

# Pick Top 1 Restaurants and Export to CSV
#-----------------------------------
review_counts = df['business_id'].value_counts().reset_index(name='review_count')
review_counts.columns = ['business_id', 'review_count']
top_1_business_ids = review_counts.head(1)['business_id']
top_1_reviews = df[df['business_id'].isin(top_1_business_ids)]
top_1_reviews.to_csv('csv/df_top1.csv', index=False)