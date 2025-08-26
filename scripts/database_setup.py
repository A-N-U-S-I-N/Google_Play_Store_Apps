import sqlite3
import pandas as pd

df = pd.read_csv('cleaned_googleplaystore.csv')

conn = sqlite3.connect('googleplaystore.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS apps (
    App TEXT,
    Category TEXT,
    Rating REAL,
    Reviews INTEGER,
    Size_in_bytes REAL,
    Installs INTEGER,
    Price REAL,
    Genres TEXT
)
''')

df[['App','Category','Rating','Reviews','Size_in_bytes','Installs','Price','Genres']] \
  .rename(columns={'Size':'Size_in_bytes'}) \
  .to_sql('apps', conn, if_exists='replace', index=False)

conn.commit()
print("Database setup and data load complete.")

conn.close()
