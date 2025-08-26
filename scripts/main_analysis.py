import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_and_clean():
    apps = pd.read_csv('googleplaystore.csv')
    reviews = pd.read_csv('googleplaystore_user_reviews.csv')

    apps.drop(10472, axis=0, inplace=True)
    apps['Reviews'] = apps['Reviews'].astype(int)

    def convert_size(size):
        if isinstance(size, str):
            if 'k' in size:
                return float(size.replace('k', '')) * 1024
            elif 'M' in size:
                return float(size.replace('M', '')) * 1024 * 1024
            elif 'Varies with device' in size:
                return np.nan
        return size

    apps['Size'] = apps['Size'].apply(convert_size)
    apps['Installs'] = apps['Installs'].str.replace('[+,]', '', regex=True).replace('Free', np.nan).astype(float)
    apps['Price'] = apps['Price'].str.replace('$', '').astype(float)

    bins = [-1, 0, 10, 1000, 10000, 100000, 1000000, 10000000, 10000000000]
    labels = ['no', 'Very low', 'Low', 'Moderate', 'More than moderate', 'High', 'Very High', 'Top Notch']
    apps['Installs_category'] = pd.cut(apps['Installs'], bins=bins, labels=labels)

    median_ratings = apps.groupby('Installs_category')['Rating'].median()

    def fill_missing_ratings(df, category, fill_value):
        filter_ = (df['Installs_category'] == category) & (df['Rating'].isna())
        df.loc[filter_, 'Rating'] = fill_value
        return df

    for cat, val in median_ratings.items():
        apps = fill_missing_ratings(apps, cat, val)

    apps.drop_duplicates(inplace=True)

    return apps, reviews

def visualize(apps):
    plt.figure(figsize=(10,6))
    sns.histplot(apps['Rating'], bins=20, kde=True)
    plt.title('Distribution of App Ratings')
    plt.savefig('rating_distribution.png')
    plt.close()

    plt.figure(figsize=(12,8))
    sns.countplot(y='Category', data=apps, order=apps['Category'].value_counts().index)
    plt.title('Count of Apps by Category')
    plt.savefig('apps_by_category.png')
    plt.close()

    plt.figure(figsize=(10,6))
    sns.scatterplot(x='Rating', y='Installs', hue='Category', data=apps, alpha=0.6)
    plt.title('Installs vs Rating by Category')
    plt.savefig('installs_vs_rating.png')
    plt.close()

def main():
    apps, reviews = load_and_clean()
    visualize(apps)
    print("Data cleaning and visualization completed. Plots saved.")

if __name__ == "__main__":
    main()
