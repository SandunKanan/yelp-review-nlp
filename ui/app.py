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
import seaborn as sns
import plotly.graph_objects as go

# Set page config
st.set_page_config(layout="wide")
################## Display - Tilte ###################
####################################################################################################
####################################################################################################

st.markdown(
"""
<style>
/* ---- Padding on header ---- */
.st-emotion-cache-z5fcl4 {
    padding-top: 1rem;
}

/* ---- Review Summery ---- */
.js-plotly-plot .plotly, .js-plotly-plot .plotly div {
    margin: -50px 0;
    z-index: 1;
}
.st-emotion-cache-1629p8f h1, .st-emotion-cache-1629p8f h2, .st-emotion-cache-1629p8f h3, .st-emotion-cache-1629p8f h4, .st-emotion-cache-1629p8f h5, .st-emotion-cache-1629p8f h6, .st-emotion-cache-1629p8f span{
z-index: 99;
}

/* ---- Column Gap ---- */
.st-emotion-cache-keje6w {
padding: 0 30px 0px 0;
}

/* ---- Logo ---- */
.st-emotion-cache-1v0mbdj {
margin: 0 auto;
}

/* ---- Header ---- */
.stTextInput > div > div {
    padding: 10px; /* You can adjust this value */
}

.stButton > button {
    width: 100%; /* Makes the button stretch to full width */
    padding: 10px; /* You can adjust this value */
}
.st-emotion-cache-r421ms {
border: none;
}
/* ---- Restaurant Name ---- */
.big-font {
    font-size:24px !important;
}
</style>
""",
    unsafe_allow_html=True,
)



# You may want to add custom styling to adjust the look and feel
# This is done using markdown and unsafe_allow_html
st.markdown("""
<style>

</style>
""", unsafe_allow_html=True)
############# Display - User Input ###################
####################################################################################################
####################################################################################################

# Set up the layout for the header
# st.title("NLPalate")
# st.caption("Select a restaurant to analyze reviews and gain insights.")

left_co,left2_co, cent_co,last2_co,last_co = st.columns([2,2,3,2,2])
with cent_co:
    st.image('ui/img/logo_nlpalate_200.png', use_column_width=True, width=180)
# Set up the form
# Create a search bar form
with st.form(key='user_input_form'):
    # Organize the inputs and button in a single column for better control
    col1,col2,col3 = st.columns([2,3,2])

    with col2:
        # Create a text input that stretches to full width
        name = st.text_input('Restaurant Name (e.g. Luke, Gumbo Shop, Royal House, Cochon)', max_chars=50)

        # Create some space between the text input and button
        st.text(" ")

        # Create a centered submit button with adjusted width
        submit_btn = st.form_submit_button('Get Results')


# Add space below the form
# st.caption("Choose from : Luke, Gumbo Shop, Commander's Palace, Royal House, Felix's Restaurant & Oyster Bar, Cochon, Mother's Restaurant, Oceana Grill, Acme Oyster House, Ruby Slipper - New Orleans")


# Read the data tables only once, not inside the conditional
df_review = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_review_top10.csv')
df_business = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_business_top10.csv')
df_praise = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_praise_top10.csv')
df_complaint = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_complaint_top10.csv')
df_wordcloud = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_wordcloud_top10.csv')
df_example = pd.read_csv('https://storage.googleapis.com/yelp_review_nlp/df_examples2_top10.csv')

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
        st.header("Restaurant Name")
        st.markdown(f'<div class="big-font">{name}</div>', unsafe_allow_html=True)
    with col2:
        st.header("Category")
        st.write(f"{df_business_filtered['categories'].iloc[0]}")
        # st.metric(label="Average Review Scores", value=average_reviews)
        # st.metric(label="Total Reviews", value=review_count)
        # st.metric(label="Average Review Score of Other Restaurants Within 10 Miles", value=avg_stars10m_radius)

    # Subheader for all plots
    st.text(" ")  # add space
    st.text(" ")  # add space
    st.text(" ")  # add space
    st.text(" ")  # add space
    st.header("Review Summary")
    col3, col4, col5 = st.columns(3)
    with col3:
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=average_reviews,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Average Review Scores"},
            gauge={'axis': {'range': [None, 5]}, 'bar': {'color': "#7d8beb"}},
            number={'font': {'color': "rgb(34, 34, 34)"}}  # Set number font color to black and adjust size as needed
        ))

        # Use Streamlit to render Plotly chart
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))  # Reducing margin/padding
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = go.Figure(go.Indicator(
            mode="number",
            value=review_count,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Total Reviews"},
            number={'font': {'color': "rgb(34, 34, 34)"}}  # Set number font color to black and adjust size as needed
        ))

        # Use Streamlit to render Plotly chart 
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))  # Reducing margin/padding
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_stars10m_radius,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': "Average Review Score of Other Restaurants Within 10 Miles",
                'font': {'size': 13}  # Adjust the size as needed
            },
            gauge={'axis': {'range': [None, 5]}, 'bar': {'color': "#cdd2f8"}},
            number={'font': {'color': "rgb(34, 34, 34)"}}  # Set number font color to black and adjust size as needed
        ))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))  # Reducing margin/padding
        st.plotly_chart(fig, use_container_width=True)
    ########## Display - Top 5 Compliments / Complaints
    ####################################################################################################
    ####################################################################################################
    # Filter and sort for top 5 praises
    col6, col7 = st.columns(2)
    with col6:
        # st.subheader("Top 5 Praises")
        # top_praises = df_praise_filtered.nlargest(5, 'praise_score')
        # fig, ax = plt.subplots()
        # sns.barplot(x='praise_score', y='praise_text', data=top_praises, ax=ax, palette="Blues_d")
        # plt.xlabel('Praise Score')
        # st.pyplot(fig)
        st.header("Top 5 Praises")
        top_praises = df_example_filtered.nlargest(5, 'praise_coeff')
        fig, ax = plt.subplots()
        sns.barplot(x='praise_coeff', y='praise_words', data=top_praises, ax=ax, palette="Blues_d")
        plt.xlabel('Praise Score')
        st.pyplot(fig)

    ####################################################################################################
    with col7:
        st.header("Top 5 Complaints")
        # Ensure the complaints are sorted in ascending order by the 'complaint_score'
        top_complaints = df_example_filtered.nsmallest(5, 'complaint_coeff')
        # Sort the DataFrame in descending order to have 'open' at the top when plotted
        # top_complaints = top_complaints.sort_values('complaint_coeff', ascending=False)
        fig, ax = plt.subplots()
        sns.barplot(x='complaint_coeff', y='complaint_words', data=top_complaints, ax=ax, palette="Reds_d")
        plt.xlabel('Complaint Score')
        st.pyplot(fig)

    ####################################################################################################
    ####################################################################################################
    st.text(" ")  # add space
    st.text(" ")  # add space
    col8, col9 = st.columns(2)
    with col8:
        st.header("Praise Examples")
        df_example_filtered_praise_order = df_example_filtered.nlargest(5, 'praise_coeff')

        for index, row in df_example_filtered_praise_order.iterrows():
            with st.expander(row['praise_words']):
                st.write(row['praise_sample_reviews'])


    ####################################################################################################
    with col9:
        st.header("Complaint Examples")
        df_example_filtered_complaint_order = df_example_filtered.nsmallest(5, 'complaint_coeff')
        for index, row in df_example_filtered_complaint_order.iterrows():
            with st.expander(row['complaint_words']):
                st.write(row['complaint_sample_reviews'])


    ####################################################################################################
    ####################################################################################################


    st.text(" ")  # add space
    st.text(" ")  # add space
    st.text(" ")  # add space
    st.text(" ")  # add space


    ########## Display - Word Clouds
    ####################################################################################################
    ####################################################################################################
    # You will need to generate the word clouds separately and display them here
    # Example for displaying images:
    col10, col11 = st.columns(2)
    with col10:
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


    with col11:
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
    st.text(" ")  # add space
    st.text(" ")  # add space

    ########## Display - Suggestions for Improvement
    ####################################################################################################
    ####################################################################################################
    # st.subheader("Suggestions for Improvement")

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

    st.markdown("""
        <div style="padding: 30px 50px; order-radius: 10px; background-color:rgb(241 243 254); border-radius:30px;">
        <h2>Suggestions for Improvement</h2>
        <b>Based on the feedback gathered from customer reviews, we propose the following areas for improvement:</b>

        <ol>
            <li><b>Speed of Service:</b> Implementing a new table management system could reduce wait times and improve the flow of service.</li>
            <li><b>Staff Training:</b> Enhancing staff training programs can lead to better customer service and a more knowledgeable team.</li>
            <li><b>Menu Diversity:</b> Expanding the menu to include a wider variety of options may satisfy a larger customer base and cater to dietary restrictions.</li>
            <li><b>Quality Control:</b> Regular checks on food quality and preparation can ensure consistency and address issues related to undercooked or overpriced dishes.</li>
            <li><b>Ambiance Enhancements:</b> Small changes to lighting, music, and seating arrangements can significantly improve the overall dining experience.</li>
        </ol>

        <p>By focusing on these key areas, the restaurant can address the most pressing concerns of its patrons, potentially leading to higher satisfaction and repeat business.</p>
        </div>
    """, unsafe_allow_html=True)
    ####################################################################################################
    ####################################################################################################


