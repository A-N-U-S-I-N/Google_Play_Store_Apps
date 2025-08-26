import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import sqlite3
from nltk.sentiment import SentimentIntensityAnalyzer

@st.cache_data
def load_app_and_reviews():
    apps = pd.read_csv('cleaned_googleplaystore.csv')
    reviews = pd.read_csv('reviews_with_sentiments.csv')
    return apps, reviews

@st.cache_resource
def load_model():
    model = joblib.load('rf_rating_predictor.pkl')
    return model

apps_df, reviews_df = load_app_and_reviews()
rating_model = load_model()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "ML Predictions", "Sentiment Analysis", "SQL Query", "Reports"])

def show_overview():
    st.title("Google Play Store Apps Overview")

    st.markdown("### Filters")
    categories = apps_df['Category'].unique()
    category_filter = st.multiselect("Filter by Category", options=categories, default=categories[:5])

    min_installs, max_installs = st.slider("Installs Range", int(apps_df['Installs'].min()), int(apps_df['Installs'].max()), (0, int(apps_df['Installs'].max())))
    min_price, max_price = st.slider("Price Range ($)", float(apps_df['Price'].min()), float(apps_df['Price'].max()), (float(apps_df['Price'].min()), float(apps_df['Price'].max())))
    min_rating, max_rating = st.slider("Rating Range", float(apps_df['Rating'].min()), float(apps_df['Rating'].max()), (float(apps_df['Rating'].min()), float(apps_df['Rating'].max())))

    filtered = apps_df[
        (apps_df['Category'].isin(category_filter)) &
        (apps_df['Installs'] >= min_installs) & (apps_df['Installs'] <= max_installs) &
        (apps_df['Price'] >= min_price) & (apps_df['Price'] <= max_price) &
        (apps_df['Rating'] >= min_rating) & (apps_df['Rating'] <= max_rating)
    ]

    st.markdown(f"### Showing {len(filtered)} apps")
    st.dataframe(filtered[['App', 'Category', 'Rating', 'Reviews', 'Installs', 'Price']].sort_values(by='Installs', ascending=False))

    st.markdown("### Rating Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered['Rating'], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

    st.markdown("### Installs vs Rating")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(data=filtered, x='Installs', y='Rating', hue='Category', alpha=0.6, ax=ax2)
    st.pyplot(fig2)

def show_ml_predictions():
    st.title("ML Predictions: Predict App Ratings")
    st.markdown("Enter app features below to predict rating:")

    reviews_input = st.number_input("Reviews", min_value=0, value=1000)
    size_input_mb = st.number_input("App Size (MB)", min_value=0.0, value=10.0)
    installs_input = st.number_input("Installs", min_value=0, value=50000)
    price_input = st.number_input("Price ($)", min_value=0.0, value=0.0)
    category_list = apps_df['Category'].unique()
    category_input = st.selectbox("Category", category_list)

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    le.fit(apps_df['Category'])
    category_enc = le.transform([category_input])[0]

    size_bytes = size_input_mb * 1024 * 1024

    features = np.array([[reviews_input, size_bytes, installs_input, price_input, category_enc]])

    pred_rating = rating_model.predict(features)[0]
    st.markdown(f"### Predicted Rating: {pred_rating:.2f} / 5.0")

def show_sentiment_analysis():
    st.title("Sentiment Analysis on User Reviews")

    st.markdown("Sentiment Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x='sentiment_label', data=reviews_df, palette='pastel', ax=ax)
    st.pyplot(fig)

    st.markdown("Filter reviews by sentiment")
    sentiment_filter = st.multiselect("Select sentiment(s)", options=['Positive', 'Negative', 'Neutral'], default=['Positive', 'Negative', 'Neutral'])

    filtered_reviews = reviews_df[reviews_df['sentiment_label'].isin(sentiment_filter)]
    st.dataframe(filtered_reviews[['App', 'Translated_Review', 'sentiment_label', 'sentiment_score']].sample(50))

def show_sql_query():
    st.title("SQL Query Interface")

    query = st.text_area("Enter your SQL query here:", value="SELECT App, Category, Rating, Installs FROM apps ORDER BY Installs DESC LIMIT 10;")

    if st.button("Run Query"):
        conn = sqlite3.connect('googleplaystore.db')
        try:
            result = pd.read_sql_query(query, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")
        conn.close()

def show_reports():
    st.title("Generate Reports")

    if st.button("Export Category Summary Excel"):
        summary = apps_df.groupby('Category').agg({
            'Rating': 'mean',
            'Installs': 'sum',
            'Reviews': 'sum'
        }).reset_index()
        summary.to_excel('app_category_summary.xlsx', index=False)
        st.success("Excel report saved as app_category_summary.xlsx")

    st.markdown("Top 10 Categories by Installs")
    summary = apps_df.groupby('Category').agg({'Installs':'sum'}).reset_index()
    top_cats = summary.sort_values('Installs', ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x='Installs', y='Category', data=top_cats, ax=ax)
    st.pyplot(fig)

if page == "Overview":
    show_overview()
elif page == "ML Predictions":
    show_ml_predictions()
elif page == "Sentiment Analysis":
    show_sentiment_analysis()
elif page == "SQL Query":
    show_sql_query()
elif page == "Reports":
    show_reports()
