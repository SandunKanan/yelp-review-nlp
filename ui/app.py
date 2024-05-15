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

st.set_page_config(layout="wide")

st.markdown(
"""
<style>
/* ---- Padding on header ---- */
.st-emotion-cache-z5fcl4 {padding-top: 1.5rem;}

/* ---- Review Summery ---- */
.js-plotly-plot .plotly, .js-plotly-plot .plotly div {
    margin: -50px 0;
    z-index: 1;
}
.st-emotion-cache-1629p8f h1, .st-emotion-cache-1629p8f h2, .st-emotion-cache-1629p8f h3, .st-emotion-cache-1629p8f h4, .st-emotion-cache-1629p8f h5, .st-emotion-cache-1629p8f h6, .st-emotion-cache-1629p8f span{
z-index: 99;
text-align: center;
}

/* ---- Column Gap ---- */
.st-emotion-cache-keje6w {padding: 0 30px 0px 0;}

/* ---- Logo ---- */
.st-emotion-cache-1v0mbdj {
margin: 0 auto;
}

/* ---- Header ---- */
.stTextInput > div > div {
    padding: 10px;
}

.stButton > .st-emotion-cache-7ym5gk {
    width: 100%;
    padding: 10px;
}
.st-emotion-cache-r421ms {
border: none;
}
/* ---- Restaurant Name ---- */
.big-font {
    font-size:24px !important;
    text-align: center;
}
/* ---- Category Name ---- */
.st-emotion-cache-eqffof p {
    text-align: center;
}
/* ---- Align Left for the review examples ---- */
.st-emotion-cache-eqffof p {
    text-align: center;
}
/* ---- Align Left for the review examples ---- */
.element-container .st-emotion-cache-eqffof p {
    text-align: left;
}

table.dataframe {
    caption-side: bottom;
    border-collapse: collapse;
    margin: 0 auto;
}
.st-emotion-cache-l9bjmx {
    font-family: "Source Sans Pro", sans-serif;
    margin: 0 auto;
}
/* ---- Change the font color for expander ---- */
.st-emotion-cache-1h9usn1 {
    background-color: #f7f7f7;
}
</style>
""",
    unsafe_allow_html=True,
)

# Session state
if "get_result" not in st.session_state:
    st.session_state["get_result"] = False
if "get_topics" not in st.session_state:
    st.session_state["get_topics"] = False
if "run_regression" not in st.session_state:
    st.session_state["run_regression"] = False
if "get_suggestions" not in st.session_state:
    st.session_state["get_suggestions"] = False


############# Display - Title / User Input ###################
left_co,left2_co, cent_co,last2_co,last_co = st.columns([2,2,3,2,2])
with cent_co:
    st.image('ui/img/logo_nlpalate_200.png', use_column_width=True, width=180)

with st.form(key='user_input_form'):
    col1,col2,col3 = st.columns([2,3,2])

    with col2:
        name = st.text_input("Restaurant Name", max_chars=50)
        st.text(" ")
        st.form_submit_button(
            'Get Results',
            on_click=lambda: st.session_state.update({"get_result": True})
        )

# Read CSV
df_review = pd.read_csv('data/df_review_top10.csv')
df_business = pd.read_csv('data/df_business2_top10.csv')
df_praise = pd.read_csv('data/df_praise_top10.csv')
df_complaint = pd.read_csv('data/df_complaint_top10.csv')
df_wordcloud = pd.read_csv('data/df_wordcloud_top10.csv')
df_example = pd.read_csv('data/df_example_top_10_b.csv')
df_lda = pd.read_csv('data/df_coefficients_lda.csv')
df_get_topics = pd.read_csv('data/df_get_topics2.csv')
df_topic_allocation = pd.read_csv('data/df_topic_allocation_with_labels.csv')

# Display the result

df_get_topics = df_get_topics[['topic_label', 'phrase', 'score']]
df_get_topics = df_get_topics.rename(columns={'topic_label': 'Topic', 'phrase': 'Phrase', 'score': 'Score'})


# Display the result
if st.session_state["get_result"]:
    df_review_filtered = df_review[df_review['name'].str.contains(name, case=False, na=False)]
    df_business_filtered = df_business[df_business['name'].str.contains(name, case=False, na=False)]
    df_praise_filtered = df_praise[df_praise['name'].str.contains(name, case=False, na=False)]
    df_complaint_filtered = df_complaint[df_complaint['name'].str.contains(name, case=False, na=False)]
    df_wordcloud_filtered = df_wordcloud[df_wordcloud['name'].str.contains(name, case=False, na=False)]
    df_example_filtered = df_example[df_example['name'].str.contains(name, case=False, na=False)]
    df_lda_filtered = df_lda[df_lda['name'].str.contains(name, case=False, na=False)]
    ############ Average reviews ############
    average_reviews = round(df_review_filtered['stars'].mean(), 1)  # Average number of stars
    review_count = len(df_review_filtered)   # Total number of reviews
    avg_stars10m_radius = round(df_review_filtered['avg_stars10m_radius'].mean(), 1)   # Avg stars in 10 mile radius

    ############ Display - Restaurant Information ############
    st.text(" ")
    st.text(" ")

    col1, col2 = st.columns(2)
    with col1:
        st.header("Restaurant Name")
        st.markdown(f'<div class="big-font">{name}</div>', unsafe_allow_html=True)
    with col2:
        st.header("Category")
        st.markdown(f"<div style='text-align: center'>{df_business_filtered['categories'].iloc[0]}</div>", unsafe_allow_html=True)

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

        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))  # Reducing margin/padding
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_stars10m_radius,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': "Other Restaurants Within 10 Miles",
                'font': {'size': 18}  # Adjust the size as needed
            },
            gauge={'axis': {'range': [None, 5]}, 'bar': {'color': "#cdd2f8"}},
            number={'font': {'color': "rgb(34, 34, 34)"}}  # Set number font color to black and adjust size as needed
        ))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))  # Reducing margin/padding
        st.plotly_chart(fig, use_container_width=True)

    ########## Display - Word Clouds ##########
    st.header("Frequently Mentioned Keywords")
    col10, col11 = st.columns(2)

    with col10:
        st.subheader("Our Restaurant")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        wc_own_dict = df_wordcloud_filtered["own_wc_dict"].iloc[0]
        wc_own_dict = ast.literal_eval(wc_own_dict)
        wc_own = WordCloud(width=800,
                      height=400,
                      background_color='white').fit_words(wc_own_dict)
        st.image(wc_own.to_array())

    with col11:
        st.subheader("Our Competitors")
        wc_other_dict = df_wordcloud_filtered["other_wc_dict"].iloc[0]
        wc_other_dict = ast.literal_eval(wc_other_dict)
        wc_other = WordCloud(width=800,
                      height=400,
                      colormap = 'BuPu_r',
                      background_color='white').fit_words(wc_other_dict)
        st.image(wc_other.to_array())

    st.text(" ")  # add space
    st.text(" ")  # add space
    st.text(" ")  # add space
    st.text(" ")  # add space
    ########## Display - Top 5 Compliments / Complaints ##########
    col6, col7 = st.columns(2)
    with col6:
        st.header("Top 5 Praises")
        top_praises = df_example_filtered.nlargest(5, 'praise_coeff')
        fig, ax = plt.subplots()
        sns.barplot(x='praise_coeff', y='praise_words', data=top_praises, ax=ax, palette="Blues_d")
        plt.xlabel('Praise Score')
        ax.set_ylabel('')  # Removes the y-axis label
        st.pyplot(fig)

    with col7:
        st.header("Top 5 Complaints")
        top_complaints = df_example_filtered.nsmallest(5, 'complaint_coeff')
        fig, ax = plt.subplots()
        sns.barplot(x='complaint_coeff', y='complaint_words', data=top_complaints, ax=ax, palette="Reds_d")
        plt.xlabel('Complaint Score')
        ax.set_ylabel('')  # Removes the y-axis label
        st.pyplot(fig)

     ########## Display - Examples ##########
    st.text(" ")  # add space
    st.text(" ")  # add space
    col8, col9 = st.columns(2)
    with col8:
        st.header("Praise Examples")
        df_example_filtered_praise_order = df_example_filtered.nlargest(5, 'praise_coeff')

        for index, row in df_example_filtered_praise_order.iterrows():
            with st.expander(row['praise_words']):
                st.write(row['praise_sample_reviews'])

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


    ########## TF-IDF Explanation ##########

    with st.expander("Show TF-IDF explanation"):
        st.write("Review 1: ‘Just serves the best pancakes in town. The service is excellent and the atmosphere is cozy.’ \n\n"
         "Review 2: ‘Just wonderful! The burgers were delicious and the staff was friendly.’ \n\n"
         "Review 3: ‘Just mediocre food and the service was slow.’ \n\n"
         "In ALL reviews, the word ‘just’ appears, so the weight TF-IDF assigns is zero. Conversely, ‘best pancakes’, "
         "‘burgers delicious’, and ‘service slow’ appear in one review, so their weight will be high. "
         "Just remember, that the word just doesn't add "
         "any value to the reviews; it's just how people talk.")
        st.image("ui/img/tf-idf.png")
    st.text(" ")  # add space
    st.text(" ")  # add space
    st.text(" ")  # add space
    st.text(" ")  # add space
    ########## Advanced Modeling ##########
    st.header("Advanced Modeling")
    ########## Get Topic ##########
    topic_weights = df_topic_allocation.groupby("topic_label", as_index=False).sum()
    topic_weights["score"] = topic_weights["score"] / df_topic_allocation["score"].sum()
    topic_weights = topic_weights.drop(columns="topic")
    topic_weights = topic_weights.sort_values(by="score", ascending=False).head(15)
    st.button(
        'Get Topics',
        on_click=lambda: st.session_state.update({"get_topics": True})
    )
    if st.session_state["get_topics"]:
        st.text(" ")  # add space
        st.text(" ")  # add space
        st.subheader("List of Topics")
        plt.figure(figsize=(10, 4)) # You can adjust these numbers as per your need
        ax = sns.barplot(
            y="topic_label",
            x="score",
            data=topic_weights,
            palette="Greens_d"
        )
        ax.tick_params(axis='y', labelsize=10)  # Adjust the size as per your need
        ax.tick_params(axis='x', labelsize=10)  # Adjust the size as per your need
        plt.xlabel("Topic Prevalence in Reviews", fontsize=12) # Adjust the font size as per your need
        plt.ylabel("Topic", fontsize=12)  # Adjust the font size as per your need
        plt.tight_layout()
        st.pyplot(plt)
        st.text(" ")  # add space
        st.text(" ")  # add space
    with st.expander("Show Topic Modelling (LDA) explanation"):
        st.text(" ")  # add space
        st.write("Latent Dirichlet Allocation (LDA) is an advanced technique used to categorize words into topics."
                 "Initially, words present in text are randomly assigned to topics, and through iterative adjustments, LDA seeks to predict the composition of the original document accurately."
                 " This process is grounded in a methodical approach where, over numerous iterations, the model identifies the allocation of words to topics that best reflects the observed text."
                 " The effectiveness of LDA stems from its ability to discern the underlying themes within texts, such as ‘service quality’ or ‘atmosphere’, from seemingly unstructured data."
                 " By automatically discovering these themes, LDA provides actionable insights into large datasets.")
        st.text(" ")  # add space
        st.image("ui/img/lda1.png")
        st.text(" ")  # add space
        st.image("ui/img/lda2.png")
        st.text(" ")  # add space

    ########## Run Regression ##########
    # df_lda_filtered_top5 = df_lda_filtered[df_lda_filtered['Coefficient Type'] == 'Top 5 Positive']
    # df_lda_filtered_bottom5 = df_lda_filtered[df_lda_filtered['Coefficient Type'] == 'Bottom 5 Negative']
    # # Get a list of features for top 5 positive
    # top_5_positive_features = df_lda_filtered_top5['Feature'].tolist()
    # # Join into a single string with a separator like a comma or line break
    # top_5_positive_features_str = ', '.join(top_5_positive_features)

    # # Get a list of features for bottom 5 negative
    # bottom_5_negative_features = df_lda_filtered_bottom5['Feature'].tolist()
    # # Join into a single string with a separator like a comma or line break
    # bottom_5_negative_features_str = ', '.join(bottom_5_negative_features)
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    st.button(
        'Run Regression',
        on_click=lambda: st.session_state.update({"run_regression": True})

    )
    if st.session_state["run_regression"]:
        # st.markdown(f"""
        #         <div style="background-color: rgb(240, 242, 246); border-radius: 10px; padding: 20px; margin: 10px 0;">
        #             <h2 style="color: #333;text-align:center;">Most Frequent Topics Mentioned</h2>
        #             <p style="text-align:center;"><b>Top 5 Positive:</b> {top_5_positive_features_str}</p>
        #             <p style="text-align:center;"><b>Bottom 5 Negative:</b> {bottom_5_negative_features_str}</p>
        #         </div>
        #         """, unsafe_allow_html=True)
        st.subheader("Topics Driving Positive/Negative Reviews")

        col6, col7 = st.columns(2)
        with col6:
            st.subheader("Top 5 Positive")
            df_lda_positive = df_lda_filtered.nlargest(5, 'Coefficient')
            fig, ax = plt.subplots()
            sns.barplot(x='Coefficient', y='Feature', data=df_lda_positive, ax=ax, palette="Blues_d")
            plt.xlabel('Positive Words')
            ax.set_ylabel('')  # Removes the y-axis label
            st.pyplot(fig)

        with col7:
            st.subheader("Top 5 Negative")
            df_lda_negative = df_lda_filtered.nsmallest(5, 'Coefficient')
            fig, ax = plt.subplots()
            sns.barplot(x='Coefficient', y='Feature', data=df_lda_negative, ax=ax, palette="Reds_d")
            plt.xlabel('Negative')
            ax.set_ylabel('')  # Removes the y-axis label
            st.pyplot(fig)



    with st.expander("Show Linear Regression Explanation"):
        st.text(" ")  # add space
        st.write("Imagine you're listening to people talk about Mother's Restaurant."
                 " Some say the ‘chicken wings are amazing’, while others complain about ‘rude service’. "
                 "All this talk goes on for a long time on places like Yelp or social media. Now, if we want to figure out how much these good or bad comments affect the restaurant's overall rating, we use something called regression."
                 " Regression is like a magic math trick. It helps us see how each thing people mention, like ‘great chicken wings’ or ‘rude service’, affects the restaurant's score giving us impact coefficients."
                 " The cool part is these coefficients tell us exactly what needs fixing to get better ratings.")
        st.text(" ")  # add space
        st.image("ui/img/linear_regression.png")
    ########## Get Suggestion ##########
    # get_suggestions = st.button('Get Suggestions')

    st.button(
        'Get Suggestions',
        on_click=lambda: st.session_state.update({"get_suggestions": True})

    )
    if st.session_state["get_suggestions"]:
        st.markdown(f"""
                <div style="background-color: rgb(240, 242, 246); border-radius: 10px; padding: 20px; margin: 10px 0;">
                    <h2 style="color: #333;text-align:center;">Suggestion for Improvement</h2>
                    <p>{df_business_filtered['ai_suggestion'].iloc[0]}</p>
                </div>
                """, unsafe_allow_html=True)





    # Display the result
    ########## Display - Suggestions for Improvement
    ############################################################################to########################
    ####################################################################################################
    # st.header("Suggestions for Improvement")

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

    # st.markdown("""
    #     <div style="padding: 30px 50px; order-radius: 10px; background-color:rgb(241 243 254); border-radius:30px;">
    #     <h2>Suggestions for Improvement</h2>
    #     <b>Based on the feedback gathered from customer reviews, we propose the following areas for improvement:</b>

    #     <ol>
    #         <li><b>Speed of Service:</b> Implementing a new table management system could reduce wait times and improve the flow of service.</li>
    #         <li><b>Staff Training:</b> Enhancing staff training programs can lead to better customer service and a more knowledgeable team.</li>
    #         <li><b>Menu Diversity:</b> Expanding the menu to include a wider variety of options may satisfy a larger customer base and cater to dietary restrictions.</li>
    #         <li><b>Quality Control:</b> Regular checks on food quality and preparation can ensure consistency and address issues related to undercooked or overpriced dishes.</li>
    #         <li><b>Ambiance Enhancements:</b> Small changes to lighting, music, and seating arrangements can significantly improve the overall dining experience.</li>
    #     </ol>

    #     <p>By focusing on these key areas, the restaurant can address the most pressing concerns of its patrons, potentially leading to higher satisfaction and repeat business.</p>
    #     </div>
    # """, unsafe_allow_html=True)
    # st.write(f"{df_business_filtered['ai_suggestion'].iloc[0]}")



    ####################################################################################################
    ####################################################################################################
