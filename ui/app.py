# import openai
import pandas as pd
# import string
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st
# import os
from wordcloud import WordCloud
# import matplotlib.pyplot as plt
import openai
import ast
import matplotlib.pyplot as plt


# Set page config
st.set_page_config(layout="wide")
################## Display - Tilte ###################
####################################################################################################
####################################################################################################


############# Display - User Input ###################
####################################################################################################
####################################################################################################

# Set up the layout for the header
st.title("NLPalette")
st.caption("Select a restaurant to analyze reviews and gain insights.")

# Set up the form
with st.form(key='user_input_form'):
    # Organize the inputs and button in two columns
    col1, col2 = st.columns([3, 1])  # Adjust the ratio based on your preference

    with col1:
        name = st.selectbox("Restaurant Name", [
            'Luke', 'Gumbo Shop', "Commander's Palace", 'Royal House',
            "Felix's Restaurant & Oyster Bar", 'Cochon', "Mother's Restaurant",
            'Oceana Grill', 'Acme Oyster House', 'Ruby Slipper - New Orleans'
        ])

    with col2:
        st.text(" ")
        st.text(" ")
        submit_btn = st.form_submit_button('Get Results')

# Add space below the form
st.text(" ")

    

# Read the data tables only once, not inside the conditional
df_review = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_review_top10.csv')
df_business = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_business_top10.csv')
df_praise = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_praise_top10.csv')
df_complaint = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_complaint_top10.csv')
df_wordcloud = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_wordcloud_top10.csv')
df_example = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_examples_top10.csv')

# Display the result
if submit_btn:
    # Filter data based on the restaurant name
    df_review_filtered = df_review[df_review['name'].str.contains(name, case=False, na=False)]
    df_business_filtered = df_business[df_business['name'].str.contains(name, case=False, na=False)]
    df_praise_filtered = df_praise[df_praise['name'].str.contains(name, case=False, na=False)]
    df_complaint_filtered = df_complaint[df_complaint['name'].str.contains(name, case=False, na=False)]
    df_wordcloud_filtered = df_wordcloud[df_wordcloud['name'].str.contains(name, case=False, na=False)]
    df_example_filtered = df_example[df_example['name'].str.contains(name, case=False, na=False)]

    ############ Average reviews
    ####################################################################################################
    ####################################################################################################
    average_reviews = round(df_review_filtered['stars'].mean(), 1)  # Average number of stars
    review_count = len(df_review_filtered)   # Total number of reviews
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

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Top 5 Praises")
        top_praises = df_praise_filtered.nlargest(5, 'praise_score')
        top_praises = top_praises.sort_values('praise_score', ascending=True)
        fig, ax = plt.subplots()
        ax.barh(top_praises['praise_text'], top_praises['praise_score'])
        plt.xlabel('Praise Score')
        st.pyplot(fig)

       # Praise Example
        st.text(" ")  # add space
        st.subheader("Praise Examples")
        praise_example_texts = df_example_filtered['praise_sample_reviews'].tolist()

        for index, row in df_example_filtered.iterrows():
            # Use the 'praise_text' as the expander label
            with st.expander(row['praise_words']):
                # Here you can show detailed examples related to the 'praise_text'
                # For now, let's show the 'praise_text' itself as an example
                st.write(row['praise_sample_reviews'])
                # If you have detailed examples, you can filter them from 'df_example_filtered' based on 'praise_text'
                # detailed_examples = df_example_filtered[df_example_filtered['some_column'] == row['praise_text']]
                # for example in detailed_examples:
                #     st.write(example['praise_sample_reviews'])


    ####################################################################################################
    with col4:
        st.subheader("Top 5 Complaints")
        top_complaints = df_complaint_filtered.nlargest(5, 'complaint_score')
        top_complaints = top_complaints.sort_values('complaint_score', ascending=False)
        fig, ax = plt.subplots()
        ax.barh(top_complaints['complaint_text'], top_complaints['complaint_score'])
        plt.xlabel('Complaint Score')
        st.pyplot(fig)

        st.subheader("Complaint Examples")
        # Complaint Examples
        # complaint_example_texts = df_example_filtered['complaint_sample_reviews'].tolist()
        # for complaint_example in complaint_example_texts:
        #     st.write(complaint_example)
        #     st.text(" ")  # add space
        #     st.text(" ")  # add space
        #     st.text(" ")  # add space
        for index, row in df_example_filtered.iterrows():
            # Use the 'praise_text' as the expander label
            with st.expander(row['complaint_words']):
                # Here you can show detailed examples related to the 'praise_text'
                # For now, let's show the 'praise_text' itself as an example
                st.write(row['complaint_sample_reviews'])
                # If you have detailed examples, you can filter them from 'df_example_filtered' based on 'praise_text'
                # detailed_examples = df_example_filtered[df_example_filtered['some_column'] == row['praise_text']]
                # for example in detailed_examples:
                #     st.write(example['praise_sample_reviews'])


    ####################################################################################################
    ####################################################################################################
        

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
        st.subheader("Frequently Mentioned Keywords from our Customers")

        # st.image('notebooks/img/mothers_1.jpg', caption='Visual Representation of Common Review Comments')

        st.set_option('deprecation.showPyplotGlobalUse', False)

        #select the WordCloud Dictionary
        wc_own_dict = df_wordcloud_filtered["own_wc_dict"].iloc[0]
        wc_own_dict = ast.literal_eval(wc_own_dict)

        #Display WordCloud
        wc_own = WordCloud(width=800,
                      height=400,
                      background_color='white').fit_words(wc_own_dict)
        st.image(wc_own.to_array())


    with col6:
        st.subheader("Frequently Mentioned Keywords at our Competitors")

        #select the WordCloud Dictionary
        wc_other_dict = df_wordcloud_filtered["other_wc_dict"].iloc[0]
        wc_other_dict = ast.literal_eval(wc_other_dict)

        #Display WordCloud
        wc_other = WordCloud(width=800,
                      height=400,
                      colormap = 'BuPu_r',
                      background_color='white').fit_words(wc_other_dict)
        st.image(wc_other.to_array())

    st.text(" ")  # add space
    st.text(" ")  # add space


    ########## Display - Suggestions for Improvement
    ####################################################################################################
    ####################################################################################################
    st.subheader("Suggestions for Improvement")

    # #####################################################

    # openai.api_key = st.secrets['OPENAI_API_KEY']

    # # Create a prompt based on the top complaints for the restaurant
    # prompt = f"The following are the top customer complaints for {name}: {complaint_texts}. Can you suggest improvements for the restaurant within 100 words?"

    # # Make a request to the API to generate text
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",  # Use the engine of your choice
    #     messages = [{"role": "user", "content": prompt}],
    #     max_tokens = 100
    # )

    # st.write(response["choices"][0]["message"]["content"])
    #####################################################

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

st.markdown(
    """
<style>

</style>
""",
    unsafe_allow_html=True,
)