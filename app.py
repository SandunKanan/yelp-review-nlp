import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st


# Set page config
st.set_page_config(layout="wide")
################## Display - Tilte ###################
st.title("NSPalete")
st.text(" ")  # add space

############# Display - User Input ###################
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
mother = pd.read_csv('notebooks/csv/df_top10.csv', index_col=0)
mother.reset_index(drop=True, inplace=True)
# mother['date'] = pd.to_datetime(mother['date'])

# Display the result
if submit_btn:
    # Filter data based on the restaurant name
    filtered_data = mother[mother['name'].str.contains(name, case=False, na=False)]
    # Filter by the selected date range
    # filtered_data = filtered_data[
    #     (filtered_data['date'] >= pd.to_datetime(date_from)) & 
    #     (filtered_data['date'] <= pd.to_datetime(date_to))
    # ]



    ############ Average reviews
    average_reviews = filtered_data['restaurant_avg_star'].mean()  # Average number of stars
    review_count = filtered_data['review_count'].mean()   # Total number of reviews
    avg_stars10m_radius = round(filtered_data['avg_stars10m_radius'].mean(), 2)   # Avg stars in 10 mile radius

    ############ Display - Restaurant Information
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Restaurant Information")
        st.write(f"**Name:** {name}")
        # st.write(f"**Category:** {filtered_data['categories'].iloc[0]}")
        
    with col2:
        st.subheader("Review Summary")
        st.metric(label="Average Review Scores", value=average_reviews)
        st.metric(label="Total Reviews", value=review_count)
        st.metric(label="Average Review Score of Other Restaurants Within a 10 Miles", value=avg_stars10m_radius)
    st.text(" ")  # add space
    st.text(" ")  # add space
    ########## Display - Top 5 Compliments / Complaints 
 
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Top 5 Complaints")
        # Dummy text for top 5 complaints
        st.text("1. Long wait times")
        st.text("2. Unfriendly staff")
        st.text("3. Incorrect orders")
        st.text("4. Poor food quality")
        st.text("5. High prices")
    with col4:
        st.subheader("Top 5 Praises")
        # Dummy text for top 5 praises
        st.text("1. Delicious food")
        st.text("2. Excellent service")
        st.text("3. Great ambiance")
        st.text("4. Quick service")
        st.text("5. Friendly staff")
    st.text(" ")  # add space
    st.text(" ")  # add space
    ########## Display - Complaint Examples
    ########## Display - Complaint Examples
    st.subheader("Complaint Examples")

    # Dummy text for complaint examples
    complaint_examples = """
    1. "Waited for over an hour before our order was taken. Extremely disappointing service."
    2. "The food was undercooked and lacked flavor. Not what I expected at all."
    3. "Our table was ignored despite the restaurant not being busy. Will not be returning."
    4. "Found a hair in my food. The staff apologized, but it ruined our dining experience."
    5. "Overpriced for the quality of food served. There are better options available nearby."
    """

    # Display the dummy text
    st.text(complaint_examples)

    st.text(" ")  # add space
    st.text(" ")  # add space


    ########## Display - Word Clouds
    # You will need to generate the word clouds separately and display them here
    # Example for displaying images:
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("WordCloud")
        # st.image(generate_word_cloud(filtered_data['complaints']), caption='Word Cloud for Complaints')
    with col6:
        st.subheader("WordCloud")
        # st.image(generate_word_cloud(filtered_data['praises']), caption='Word Cloud for Praises')




    ########## Display - Suggestions for Improvement
    st.subheader("Suggestions for Improvement")
    # Your code for displaying suggestions for improvement here



# Function for generating word clouds (implement this according to your needs)
def generate_word_cloud(data):
    # Your word cloud generation logic here
    pass

