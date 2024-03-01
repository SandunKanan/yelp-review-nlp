import openai
import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st
import os
from dotenv import load_dotenv
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the .env file
load_dotenv()

# Set page config
st.set_page_config(layout="wide")
################## Display - Tilte ###################
####################################################################################################
####################################################################################################
st.title("NSPalete")
st.text(" ")  # add space

############# Display - User Input ###################
####################################################################################################
####################################################################################################
with st.form(key='user_input_form'):
    # Use st.columns to organize the inputs into three columns within the form
    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.selectbox("Restaurant Name", [
            'Luke', 'Gumbo Shop', "Commander's Palace", 'Royal House',
            "Felix's Restaurant & Oyster Bar", 'Cochon', "Mother's Restaurant",
            'Oceana Grill', 'Acme Oyster House', 'Ruby Slipper - New Orleans'
        ])

    with col2:
        date_from = st.date_input("Date From")

    with col3:
        date_to = st.date_input("Date To")

    # Place the submit button inside the form context but outside the columns
    submit_btn = st.form_submit_button('Get Results')

# Read the data tables only once, not inside the conditional
df_review = pd.read_csv('notebooks/csv/df_review_top10.csv')
df_business = pd.read_csv('notebooks/csv/df_business_top10.csv')
df_praise = pd.read_csv('notebooks/csv/df_praise_top10.csv')
df_complaint = pd.read_csv('notebooks/csv/df_complaint_top10.csv')


# Display the result
if submit_btn:
    # Filter data based on the restaurant name
    df_review_filtered = df_review[df_review['name'].str.contains(name, case=False, na=False)]
    df_business_filtered = df_business[df_business['name'].str.contains(name, case=False, na=False)]
    df_praise_filtered = df_praise[df_praise['name'].str.contains(name, case=False, na=False)]
    df_complaint_filtered = df_complaint[df_complaint['name'].str.contains(name, case=False, na=False)]
    # Filter by the selected date range
    # df_review_filtered = df_review_filtered[
    #     (df_review_filtered['date'] >= pd.to_datetime(date_from)) & 
    #     (df_review_filtered['date'] <= pd.to_datetime(date_to))
    # ]

    ############ Average reviews
    ####################################################################################################
    ####################################################################################################
    average_reviews = df_review_filtered['restaurant_avg_star'].mean()  # Average number of stars
    review_count = int(df_review_filtered['review_count'].mean())   # Total number of reviews
    avg_stars10m_radius = round(df_review_filtered['avg_stars10m_radius'].mean(), 1)   # Avg stars in 10 mile radius

    ############ Display - Restaurant Information
    ####################################################################################################
    ####################################################################################################
    st.text(" ")
    st.text(" ")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Restaurant Information")
        st.write(f"**Name:** {name}")
        st.write(f"**Category:** {df_business_filtered['categories'].iloc[0]}")
        
    with col2:
        st.subheader("Review Summary")
        st.metric(label="Average Review Scores", value=average_reviews)
        st.metric(label="Total Reviews", value=review_count)
        st.metric(label="Average Review Score of Other Restaurants Within a 10 Miles", value=avg_stars10m_radius)
    st.text(" ")  # add space
    st.text(" ")  # add space
    ########## Display - Top 5 Compliments / Complaints 
    ####################################################################################################
    ####################################################################################################
    # Filter and sort for top 5 praises
    
    col3, col4, col5 = st.columns([2, 2, 4])
    with col3:
        st.subheader("Top 5 Praises")
        top_praises = df_praise_filtered.nlargest(5, 'praise_score')
        praise_texts = top_praises['praise_text'].tolist()
        for praise in praise_texts:
            st.write(praise)
        # st.write(top_praises[['praise_text']])
    ####################################################################################################
    ####################################################################################################
    with col4:
        st.subheader("Top 5 Complaints")
        top_complaints = df_complaint_filtered.nsmallest(5, 'complaint_score')
        complaint_texts = top_complaints['complaint_text'].tolist()
        for complaint in complaint_texts:
            st.write(complaint)
    ####################################################################################################
    ####################################################################################################
    with col5:
        st.subheader("Complaint Examples")

        # Dummy text for complaint examples
        complaint_examples = """
        1. "Waited for over an hour before our order was taken. Extremely disappointing service."
        2. "The food was undercooked and lacked flavor. Not what I expected at all."
        3. "Our table was ignored despite the restaurant not being busy. Will not be returning."
        4. "Found a hair in my food. The staff apologized, but it ruined our dining experience."
        5. "Overpriced for the quality of food served. There are better options available nearby."
        """
        st.text(complaint_examples)

    # Display the dummy text
    
    st.text(" ")  # add space
    st.text(" ")  # add space


    st.text(" ")  # add space


    ########## Display - Word Clouds
    ####################################################################################################
    ####################################################################################################
    # You will need to generate the word clouds separately and display them here
    # Example for displaying images:
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("WordCloud of the restaurant")
        # st.image('notebooks/img/mothers_1.jpg', caption='Visual Representation of Common Review Comments')

        st.set_option('deprecation.showPyplotGlobalUse', False)

        # Create some sample text
        
        text = 'Fun, fun, awesome, awesome, tubular, astounding, superb, great, amazing, amazing, amazing, amazing'

        # Create and generate a word cloud image:
        wordcloud = WordCloud().generate(text)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    # def remove_meaningless_words(list_of_tuples) -> tuple[str, float]:
    #     # Define the set of meaningless words to be removed
    #     meaningless_words = {
    #         'new orleans', 'food came', 'back next', 'right next', 
    #         'tasted like', 'gave us', 'next door', 'even though',
    #         'time new', 'decided try', 'canal street', 'make sure',
    #         'time new orleans', 'new orleans food', 'made us', 'place eat', 
    #         'took minutes', 'across street', 'go wrong', 'wait staff', 
    #         'food always', 'place go', 'minute wait', 'wait go', 'told us', 
    #         'neighborhood restaurant'
    #     }
    
    #     # Filter the list to exclude meaningless words
    #     return [(word, score) for word, score in sorted_tfidf_list if word not in meaningless_words] 

    # def wordcloud_of_res(name:str) -> WordCloud:
    #     new_orleans_restaurants = df_business_filtered[df_business_filtered['categories'].str.contains('restaurant', case=False, na=False)]
    #     user_restaurant = new_orleans_restaurants[new_orleans_restaurants['name'] == name]
    #     user_restaurant_reviews = pd.merge(df_review_filtered, user_restaurant, on='business_id')
    #     user_restaurant_reviews['clean_text'] = user_restaurant_reviews['text'].apply(clean)
    #     vectors = pd.DataFrame(vectorizer.transform(user_restaurant_reviews.clean_text).toarray(),
    #                     columns = vectorizer.get_feature_names_out())
    #     sum_tfidf = vectors.sum(axis=0).sort_values(ascending=False)
    #     tfidf_list = [(word, sum_tfidf[word]) for word, idx in vectorizer.vocabulary_.items()]
    #     sorted_tfidf_list =sorted(tfidf_list, key = lambda x: x[1], reverse=True)
    #     tfidf_list_clean = remove_meaningless_words(sorted_tfidf_list)
    #     word_scores = dict(tfidf_list_clean) 
    #     wordcloud = WordCloud(width=800, 
    #                         height=400, 
    #                         colormap = 'BuPu_r',
    #                         background_color='white').generate_from_frequencies(word_scores)
    #     plt.figure(figsize=(10, 6))
    #     plt.imshow(wordcloud, interpolation='bilinear')
    #     plt.axis("off");
    #     st.pyplot()
    
    # wordcloud_of_res(name)


    with col6:
        st.subheader("WordCloud of other restaurants in same category")
        # st.image('notebooks/img/mothers_2.jpg', caption='Visual Representation of Common Review Comments from other restaurants in same category')
        st.set_option('deprecation.showPyplotGlobalUse', False)

        # Create some sample text
        text = 'Fun, fun, awesome, awesome, tubular, astounding, superb, great, amazing, amazing, amazing, amazing'

        # Create and generate a word cloud image:
        wordcloud = WordCloud().generate(text)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    st.text(" ")  # add space
    st.text(" ")  # add space
    ####################################################################################################
    ####################################################################################################


    ########## Display - Suggestions for Improvement
    ####################################################################################################
    ####################################################################################################
    st.subheader("Suggestions for Improvement")

    # #####################################################
    # # Function to call the OpenAI API

    # openai.api_key = os.getenv('OPENAI_API_KEY')

    # # Create a prompt based on the top complaints for the restaurant
    # prompt = f"The following are the top customer complaints for {name}: {complaint_texts}. Can you suggest improvements for the restaurant within 100 words?"

    # # Make a request to the API to generate text
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",  # Use the engine of your choice
    #     messages = [{"role": "user", "content": prompt}],
    #     max_tokens = 200
    # )

    # st.write(response["choices"][0]["message"]["content"])
    # #####################################################

    # Dummy Text to save the cost from ChatGPT-API
    st.write("""
    Based on the feedback gathered from customer reviews, we propose the following areas for improvement:

    1. **Speed of Service**: Implementing a new table management system could reduce wait times and improve the flow of service.
    2. **Staff Training**: Enhancing staff training programs can lead to better customer service and a more knowledgeable team.
    3. **Menu Diversity**: Expanding the menu to include a wider variety of options may satisfy a larger customer base and cater to dietary restrictions.
    4. **Quality Control**: Regular checks on food quality and preparation can ensure consistency and address issues related to undercooked or overpriced dishes.
    5. **Ambiance Enhancements**: Small changes to lighting, music, and seating arrangements can significantly improve the overall dining experience.

    By focusing on these key areas, the restaurant can address the most pressing concerns of its patrons, potentially leading to higher satisfaction and repeat business.
    """)
    ####################################################################################################
    ####################################################################################################
