import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

reviews = pd.read_csv('googleplaystore_user_reviews.csv')

reviews = reviews.dropna(subset=['Translated_Review'])

sia = SentimentIntensityAnalyzer()

reviews['sentiment_score'] = reviews['Translated_Review'].apply(lambda x: sia.polarity_scores(x)['compound'])

def sentiment_label(score):
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

reviews['sentiment_label'] = reviews['sentiment_score'].apply(sentiment_label)

plt.figure(figsize=(8,6))
sns.countplot(data=reviews, x='sentiment_label')
plt.title('Sentiment Distribution of User Reviews')
plt.show()

stopwords = set(STOPWORDS)
for sentiment in ['Positive', 'Negative']:
    text = ' '.join(reviews[reviews['sentiment_label'] == sentiment]['Translated_Review'])
    wordcloud = WordCloud(stopwords=stopwords, background_color='white', max_words=100).generate(text)
    plt.figure(figsize=(10,6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Wordcloud for {sentiment} Reviews')
    plt.show()

reviews.to_csv('reviews_with_sentiments.csv', index=False)
print("Sentiment analysis completed and saved.")
