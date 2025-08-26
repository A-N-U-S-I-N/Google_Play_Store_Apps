import sqlite3
import pandas as pd

def run_query(query):
    with sqlite3.connect('googleplaystore.db') as conn:
        result = pd.read_sql_query(query, conn)
    return result

query_top_10 = '''
SELECT App, Category, Installs
FROM apps
ORDER BY Installs DESC
LIMIT 10;
'''
top_apps = run_query(query_top_10)
print(top_apps)

query_top_installs = '''
SELECT App, Category, Installs
FROM apps
ORDER BY Installs DESC
LIMIT 5;
'''
print(run_query(query_top_installs))

query_avg_rating = '''
SELECT Category, ROUND(AVG(Rating),2) AS avg_rating, COUNT(*) as app_count
FROM apps
GROUP BY Category
ORDER BY avg_rating DESC
LIMIT 10;
'''
print(run_query(query_avg_rating))
