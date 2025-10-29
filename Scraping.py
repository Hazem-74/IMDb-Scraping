import time
from selenium import webdriver
import json
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Setup Selenium WebDriver
service = Service(executable_path= "C:/Users/Hazem/Downloads/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Define the headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# URL of the IMDb Top 250 page
url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
driver.get(url)

# Scroll to the bottom to ensure all content is loaded
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait to load the page
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Get page source and close the browser
page = driver.page_source
time.sleep(10)
driver.quit()
soup = BeautifulSoup(page, 'html.parser')

# Find the JSON data embedded in the HTML
script_tag = soup.find('script', type='application/json')
if script_tag:
    json_data = json.loads(script_tag.string)

# Extract relevant data from the JSON
movies = json_data['props']['pageProps']['pageData']['chartTitles']['edges']

# Lists to store the data
Name = []
Certificate = []
Year = []
Rate = []
Votes = []
Link = []
Genres = []
Plot = []

for movie in movies:
    movie_node = movie['node']

    # Extract movie details
    name = movie_node['titleText']['text']
    certificate = movie_node['certificate']['rating'] if movie_node.get('certificate') else "N/A"
    year = movie_node['releaseYear']['year']
    rate = movie_node['ratingsSummary']['aggregateRating']
    votes = movie_node['ratingsSummary']['voteCount']
    link = f"https://www.imdb.com/title/{movie_node['id']}/"
    genres = ", ".join([genre['genre']['text'] for genre in movie_node['titleGenres']['genres']])
    plot = movie_node['plot']['plotText']['plainText'] if movie_node['plot'] else "N/A"

    Name.append(name)
    Certificate.append(certificate)
    Year.append(year)
    Rate.append(rate)
    Votes.append(votes)
    Link.append(link)
    Genres.append(genres)
    Plot.append(plot)

#scraping more info
Directors = []
Writers = []
Actors = []
Storyline = []

for link in Link:
    page = requests.get(link, headers=headers)
    src = page.content
    soup = BeautifulSoup(src, 'lxml')

    Storyline.append(soup.find('div',{'class':'ipc-html-content-inner-div'}).text.strip())
    Directors.append(soup.find('a',{'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'}).text.strip())

    # Extract actors
    Actors_list = soup.find_all('a', {'data-testid': 'title-cast-item__actor', 'class': 'sc-bfec09a1-1 gCQkeh'})
    Actors_list_filtered = []
    for i in range(len(Actors_list)):
        Actors_list_filtered.append(Actors_list[i].text.strip())
    Actors.append('\n'.join(Actors_list_filtered))

    # Extract writers
    writers_list = soup.find_all('a', {'class': 'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link','role':'button','tabindex':'0'})
    writers_list_filtered = []
    for i in range(len(writers_list)):
        writers_list_filtered.append(writers_list[i].text.strip())

    # Check if any writer is also in Actors list and remove them
    if any(writer in Actors_list_filtered for writer in writers_list_filtered):
        writers_list_filtered = [writer for writer in writers_list_filtered if writer not in Actors_list_filtered]

    Writers.append('\n'.join(writers_list_filtered[1:3]))

# Create DataFrame
df = pd.DataFrame({
    'Name': Name,
    'Certificate': Certificate,
    'Year': Year,
    'Rate': Rate,
    'Votes': Votes,
    'Link': Link,
    'Genres': Genres,
    'Plot': Plot,
    'Writers': Writers,
    'Directors': Directors,
    'Actors': Actors,
    'Storyline': Storyline
})
df.to_csv('IMDb_Top_Movies.csv', index=False)
print(df.head())