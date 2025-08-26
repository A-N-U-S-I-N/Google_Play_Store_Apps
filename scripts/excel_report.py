import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_googleplaystore.csv')

summary = df.groupby('Category').agg({
    'Rating': 'mean',
    'Installs': 'sum',
    'Reviews': 'sum'
}).reset_index()

summary.to_excel('app_category_summary.xlsx', index=False)

plt.figure(figsize=(12,8))
summary_sorted = summary.sort_values('Installs', ascending=False).head(10)
plt.barh(summary_sorted['Category'], summary_sorted['Installs'])
plt.xlabel('Total Installs')
plt.title('Top 10 Categories by Installs')
plt.savefig('top_categories_installs.png')
plt.close()

print("Excel report and plot saved.")
