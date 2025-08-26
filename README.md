# Google Play Store Apps Data Analytics Project

## Overview
This project provides a comprehensive exploratory data analysis, machine learning modeling, sentiment analysis, and visualization of Google Play Store apps using Python, SQL, Excel, and an interactive Streamlit dashboard. The goal is to derive actionable insights on app ratings, reviews, installs, and user sentiments to support data-driven decisions for Android app developers and businesses.

## Summary of Analysis and Visualizations

### Key Visuals

#### Top 10 Categories by Installs
![Top 10 Categories by Installs](outputs/top_categories_installs.jpg)  
Shows the dominance of categories like `GAME` and `COMMUNICATION` in terms of total installs.

#### Correlation Heatmap
![Correlation Heatmap](outputs/heatmap.jpg)  
Highlights weak to moderate correlations between app features such as Reviews and Installs.

#### Count of Apps by Category
![Count of Apps by Category](outputs/apps_by_category.jpg)  
Displays distribution of apps, with `FAMILY` and `GAME` being the most numerous categories.

#### Installs vs. Rating by Category
![Installs vs Rating](outputs/installs_vs_rating.jpg)  
Scatter plot illustrating relationship between install counts and user ratings across categories.

#### Distribution of App Ratings
![Rating Distribution](outputs/rating_distribution.jpg)  
Shows a skew toward higher ratings around 4.0 to 4.5, typical for app store data.

## Getting Started

### Prerequisites
- Python 3.8+
- Pip package manager

### Installation
1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies : pip install -r requirements.txt

### Launch Streamlit Dashboard

streamlit run streamlit_app/app.py

### Use sidebar navigation to explore:

- Overview of apps with filters
- ML model predictions
- Sentiment analysis visualization
- Execute SQL queries interactively
- Export and view reports

