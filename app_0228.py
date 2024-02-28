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

    ############ Preprocess - Vectorizing Text ###########
    # vectorizer = TfidfVectorizer(ngram_range=(1,3))
    # vectorized_text = vectorizer.fit_transform(mother['clean_text'])
    # vectorized_text = pd.DataFrame(
    #     vectorized_text.toarray(),
    #     columns = vectorizer.get_feature_names_out()
    # )

    ############ Modeling - Vectorizing Text 
    # mother_1 = mother[mother['stars'] == 1]
    # mother_5 = mother[mother['stars'] == 5]
    # mother_1_vectorized = vectorizer.fit_transform(mother_1['clean_text'])
    # mother_1_vectorized = vectorizer.fit_transform(mother_1['clean_text'])
    # mother_1_vectorized = pd.DataFrame(
    #     mother_1_vectorized.toarray(),
    #     columns = vectorizer.get_feature_names_out()
    # )

    # mother_5_vectorized = vectorizer.fit_transform(mother_5['clean_text'])
    # mother_5_vectorized = pd.DataFrame(
    #     mother_5_vectorized.toarray(),
    #     columns = vectorizer.get_feature_names_out()
    # )
    # total_scores = vectorized_text.sum()
    # total_scores_1 = mother_1_vectorized.sum()
    # total_scores_5 = mother_5_vectorized.sum()
    # vectorised_comparison = pd.DataFrame(total_scores[total_scores > 0.5], columns=['total']).join(
    #     pd.DataFrame(total_scores_1[total_scores_1 > 1], columns=['1_star'])
    # ).join(
    #     pd.DataFrame(total_scores_5[total_scores_5 > 1], columns=['5_star'])
    # )
    # vectorised_comparison.fillna(0, inplace=True)
    # ratio_1 = vectorised_comparison['1_star'] / vectorised_comparison['total']
    # ratio_5 = vectorised_comparison['5_star'] / vectorised_comparison['total']
    # ration_1_sorted = ratio_1.sort_values(ascending=False)[:20]
    # ration_5_sorted = ratio_5.sort_values(ascending=False)[:20]

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



    # st.title("Top 5 Praises")
    # st.write("How people like this restaurant")
    # st.dataframe(ration_5_sorted.head(5))

    # st.title("Top 5 Complaints")
    # st.write("How people hate this restaurant")
    # st.dataframe(ration_1_sorted.head(5))

