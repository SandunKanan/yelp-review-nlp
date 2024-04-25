# Yelp Sentiment Analysis using Natural Language Processing Modelling

### Website
[NLPalate](https://yelp-nlpalate.streamlit.app/)

### Presentation Video
https://youtu.be/ixF0VNFOFC8?feature=shared&t=3252
This project was presented as a final Data Science & AI project for LeWagon Tokyo's Demo day, for the graduating cohort of March 2024

### Project Presentation
[View GoogleSlides Presentation](https://docs.google.com/presentation/d/1Dd6LnDLeSySS5ePxq6UU9FqNN78-lAZCRejmnD34oHk/edit?usp=sharing)

## Table of contents
- [Description](#description)
- [Technologies Used](#technologies-used)
  - [Libraries](#libraries)
  - [NLP Techniques and Models](#nlp-techniques-and-models)
  - [Development Environment](#development-environment)
  - [APIs and External Services](#apis-and-external-services)
  - [Frontend](#frontend)
- [Key Features of NLPalate](#key-features-of-nlpalate)
- [Installation Instructions](#installation-instructions)
- [Limitations](#limitations)
  - [Scope of Data](#scope-of-data)
  - [Data Preprocessing](#data-preprocessing)
  - [Web App Functionality](#web-app-functionality)
  - [Implications](#implications)
- [Future Work](#future-work)
- [Project Status](#project-status)
  - [Current State](#current-state)
  - [Achievements](#achievements)
  - [Challenges](#challenges)
  - [Future Work](#future-work)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## Description
This project explores the sentiment of [Yelp reviews](https://www.yelp.com/dataset) in the US to provide aggregated insights for restaurant owners, guiding them in decision making to better allocate resources to pinpoint issues and optimize performance.

## Technologies used
This project leverages a variety of technologies, libraries, and tools focused on data science and natural language processing (NLP), built with Python 3.10.6. Here's an overview of the foundational elements:

### Libraries:
- **Data Manipulation and Analysis:** Pandas for handling and analyzing data structures.
- **Visualization:** WordCloud for generating word clouds, Matplotlib & Seaborn for creating statistical graphics, and Plotly for interactive visualizations.
- **Machine Learning & NLP:** Scikit-learn for machine learning algorithms, NLTK for natural language processing tasks.
- **Web Application:** Streamlit for developing interactive web apps to showcase the NLP models.

### NLP Techniques and Models:
- **Topic Modeling:** LDA (Latent Dirichlet Allocation) to discover abstract topics within text data.
- **Text Vectorization:** TF-IDF (Term Frequency-Inverse Document Frequency) for converting text to a meaningful vector of numbers.
- **Predictive Modeling:** Linear Regression to predict outcomes based on text data.

### Development Environment:
- **Jupyter Notebook:** Used for interactive model development and experimentation.
- **Visual Studio Code:** Employed for packaging the model and further development, including the frontend.

### APIs and External Services:
- **OpenAI Public API:** Engaged to enrich the application with actionable suggestions for restaurant owners through advanced NLP capabilities.

### Frontend:
- **Streamlit:** Employed a user-friendly interface for interacting with the backend models, facilitating real-time input and feedback from users.

## Key Features of NLPalate
- Displaying an overview of key metrics (total number of reviews, restaurant's average review score, average review score of competitors within 10-mile radius) 
- Generating WordClouds of frequently-mentioned keywords in reviews of reference's restaurant compared with competitors within the same categories in the same city using unsupervised learning algorithm -- term frequency–inverse document frequency (tf-idf)
- Displaying the Top 5 Complaints and Top 5 Compliments that are affecting the restaurant with actual example of the reviews from customers
- Finding the 30 most prevalent topics in all reviews, through topic modelling using Latent Dirichlect Allocation (LDA), and unsupervised machine learning algorithm
- Performing Linear regression to map which topics and having the biggest impact on a restaurant's review score
- Aiding restaurant owners by providing focused and easily digestible recommendations/ suggestions based on the issues/ complaints they received using OpenAI's API

## Installation instructions
To get this project up and running on your local machine, follow these steps. These instructions assume you have Python 3.10.6 installed. If not, please install Python from python.org first.

### 1. Clone the Repository
Start by cloning the repository to your local machine. Open a terminal and run:
```bash
git clone https://github.com/yourusername/yelp-sentiment-analysis.git
cd yelp-sentiment-analysis
```
Replace https://github.com/yourusername/yelp-sentiment-analysis.git with the actual URL of your GitHub repository.

### 2. Setting Up a Virtual Environment with pyenv
It's recommended to manage Python versions and virtual environments using pyenv. This ensures that project dependencies do not interfere with system-wide Python packages. If you haven't already, install pyenv by following the instructions on pyenv's GitHub repository.

After installing pyenv, follow these steps to set up a virtual environment for the project:
##### 1. Install Python 3.10.6 using pyenv (skip this step if you already have this version installed):
```bash
pyenv install 3.10.6
```
##### 2. Create a virtual environment named yelp-sentiment-analysis (or another name of your choice) using Python 3.10.6:
```bash
pyenv virtualenv 3.10.6 yelp-sentiment-analysis
```
##### 3. Activate the virtual environment. Navigate to your project's directory, then set the local Python version to your newly created virtual environment:
```bash
cd path/to/yelp-sentiment-analysis
pyenv local yelp-sentiment-analysis
```
This step will create a .python-version file in your project directory, automatically activating the yelp-sentiment-analysis virtual environment whenever you navigate to this directory.
##### 4. Verify that the virtual environment is activated by checking the Python version:
```bash
python --version
```
This command should output Python 3.10.6, indicating that the correct version of Python is being used.

### 3. Install Dependencies
Install all the dependencies listed in requirements.txt:
```bash
pip install -r requirements.txt
```
Ensure you have a requirements.txt file in your repository with all the necessary libraries, including Pandas, WordCloud, Matplotlib, Seaborn, Plotly, Scikit-learn, NLTK, and Streamlit.

### 4. Set Up the Streamlit Application
To run the Streamlit application, navigate to the directory containing your Streamlit script (e.g., app.py) and execute:
```bash
streamlit run app.py
```

### 5. Accessing OpenAI API
To use the OpenAI Public API, you need an API key. Please visit OpenAI API for instructions on how to obtain one. Once you have your API key, ensure you store it securely and use it to authenticate your API requests as per OpenAI's documentation.
```bash
streamlit run app.py
```

## Limitations
This project was developed as a proof of concept to demonstrate the potential of using Natural Language Processing (NLP) for analyzing Yelp reviews and providing aggregated insights to restaurant owners. As such, there are a few limitations to be aware of:

### Scope of Data
- **Limited Dataset:** The analysis and insights generated by this project are currently based on a curated dataset comprising only 10 restaurants located in the New Orleans area. These restaurants were selected based on the volume of reviews they received (restaurants with the most number of reviews), aiming to ensure a rich dataset for analysis. The 10 restaurants are: Luke, Royal House, Commander's Palace, Gumbo Shop, Felix's Restaurant & Oyster Bar, Cochon, Mother's Restaurant, Oceana Grill, Acme Oyster House, Ruby Slipper - New Orleans

### Data Preprocessing
- **Static Preprocessing:** The reviews for these restaurants have been preprocessed, and the results have been saved as CSV files. This preprocessing step includes techniques such as tokenization, removal of stop words, and normalization, which are crucial for NLP tasks. However, the preprocessing is not dynamically applied to new data, meaning the web app's insights are static and based solely on the preprocessed dataset.

### Web App Functionality
- **Specificity to Selected Restaurants:** Given the project's proof-of-concept nature, the web app is designed to work exclusively with the data from the 10 specified restaurants. As such, it does not currently support real-time analysis or the inclusion of additional restaurants beyond this curated set.

### Implications
These limitations mean that while the project successfully demonstrates the applicability of NLP techniques for sentiment analysis in the restaurant industry, its current implementation is not scalable or directly applicable to a broader set of restaurants without further development. The static nature of the dataset and the web app's focus on a small number of restaurants restrict the direct application of this tool by other restaurant owners or stakeholders interested in gaining similar insights for different establishments.

## Project Status
### Current State
As of the last update, this project is in a proof-of-concept stage. Developed over an intensive two-week sprint by a dedicated team, the focus was on demonstrating the feasibility and potential impact of applying Natural Language Processing (NLP) techniques to analyze Yelp reviews for restaurant owners. Due to the ambitious scope and the computational resources required, the current implementation of our web application is limited to analyzing data from a select group of 10 restaurants in the New Orleans area in the US.

### Achievements
Despite the constrained timeline, the project successfully:

- Implements key NLP techniques such as LDA topic modeling, TF-IDF, and linear regression to extract actionable insights from Yelp reviews.
- Establishes a fully functional web application that showcases the utility of NLP in deriving meaningful patterns and suggestions from customer feedback.
- Demonstrates the application's potential to aid restaurant owners in decision-making by highlighting prevalent topics and sentiments in reviews.

### Challenges
The primary challenge faced was the computational limitation. Processing a larger dataset with more restaurants would require significantly more computational power and potentially more sophisticated data handling and processing strategies, which were not feasible within the project's timeframe.

### Future Work
Recognizing these limitations, future iterations of this project could include:

- **Scalability:** Exploring more efficient data processing and storage solutions to include a broader selection of restaurants and reviews.
- **Dynamic Analysis:** Implementing functionality to dynamically fetch and analyze new reviews, providing up-to-date insights.
- **Geographical Expansion:** Expanding the scope beyond New Orleans to include restaurants across various regions, offering a wider perspective on customer sentiment.

## Authors
- **Sandun Kanagama** - [SandunKanan](https://github.com/SandunKanan)

- **Sophia Tsoi** - [KZ0PHA](https://github.com/KZ0PHA)

- **Shohei Omoto** - [omotoshohei](https://github.com/omotoshohei)

- **René Osorio** - [reneosorio77](https://github.com/reneosorio77)

## Acknowledgments
- Special thanks to Xavier Fontaine, Juan Garassino, Andrii Gegliuk, Yusuke Ishida for their guidance throughout the development of this project.
- Gratitude to Sylvain Pierre, Jaris Fenner, Réda Kassi Lahlou for feedback that greatly improved the application.
