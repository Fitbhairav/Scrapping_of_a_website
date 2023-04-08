import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import datetime

# Define the URL of the webpage to be scraped
url = 'https://www.theverge.com/'

# Define the current date to be used in the CSV and database filenames
current_date = datetime.date.today().strftime("%d%m%Y")

# Define the filenames for the CSV and database
filename_csv = current_date + '_verge.csv'
filename_db = current_date + '_verge.db'

# Define the header for the CSV file
header = ["id", "URL", "headline", "author", "date"]

# Create an empty list to store the articles
articles = []

# Make a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the article elements on the page
article_list = soup.find_all('article')

# Loop through the article elements and extract the data
for i, article in enumerate(article_list):
    article_data = {}
    article_data['id'] = i + 1
    article_data['URL'] = article.find('a')['href']
    article_data['headline'] = article.find('h2').text.strip()
    article_data['author'] = article.find('span', class_='c-byline__author-name').text.strip()
    article_data['date'] = article.find('time')['datetime']
    articles.append(article_data)
articles = []
for article in soup.find_all('article'):
    headline = article.find('h2').text.strip()
    url = article.find('a')['href']
    author = article.find('span', class_='c-byline__item').text.strip()
    date = article.find('time')['datetime']
    articles.append((url, headline, author, date))
    print(headline, url, author, date)

# Write the data to the CSV file
with open(filename_csv, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    for article in articles:
        writer.writerow(article)

# Create a connection to the SQLite database
conn = sqlite3.connect(filename_db)

# Create a cursor object
cursor = conn.cursor()

# Create the table in the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        URL TEXT,
        headline TEXT,
        author TEXT,
        date TEXT
    )
''')

# Insert the data into the table
for article in articles:
    cursor.execute('INSERT INTO articles (id, URL, headline, author, date) VALUES (?, ?, ?, ?, ?)',
                   (article['id'], article['URL'], article['headline'], article['author'], article['date']))

# Commit the changes and close the connection
conn.commit()
conn.close()

print('Scraping complete.')
