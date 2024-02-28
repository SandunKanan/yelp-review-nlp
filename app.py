import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st

################## Display - Tilte ###################
st.title("Review Checker")

############# Display - User Input ###################
with st.form(key='form'):
    name = st.text_input("Restaurant Name - Choose from ①Oceana Grill ②Acme Oyster House　③Ruby Slipper - New Orleans ")
    submit_btn = st.form_submit_button('Enter')
    # reset_btn = st.form_submit_button('Reset')

########　Filter the restaurant ###########

if submit_btn:
    # Read the data tables
    mother = pd.read_csv('csv/df_top3.csv', index_col=0)
    mother.reset_index(drop=True, inplace=True)

    # Assuming there's a column 'restaurant_name' in your CSV to match user input
    mother = mother[mother['name'].str.contains(name, case=False, na=False)]

    ############ Average reviews
    average_reviews = mother['restaurant_avg_star'].mean()  # Average number of stars
    review_count = mother['review_count'].mean()   # Total number of reviews
    avg_stars10m_radius = mother['avg_stars10m_radius'].mean()   # Total number of reviews

    ########## Display - Top 5 Compliment / Complaints 

    st.title("Name of the Restaurant")
    st.write(f"{name}")

    st.title("Average Review")
    st.write(f"Restaurant's Average Review Score: {average_reviews}")

    st.title("Total Number of Reviews")
    st.write(f"Total Number of Reviews: {review_count}")

    st.title("Avg review score of other restaurants in the same category within 10 miles radius")
    st.write(f"Avg review score of other restaurants in the same category within 10 miles radius: {avg_stars10m_radius}")


