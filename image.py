import os
import requests
from bs4 import BeautifulSoup

def scrape_images(url, page_number, folder_name='scraped_images3'):
    # Create a folder to save images if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Create a folder for the current page
    page_folder = os.path.join(folder_name, f'page_{page_number}')
    os.makedirs(page_folder, exist_ok=True)

    # Define the headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor tags with image URLs
    img_tags = soup.find_all('a', href=True)

    # Extract and download image URLs
    for i, img_tag in enumerate(img_tags):
        img_url = img_tag['href']
        if img_url.endswith(('.jpg/')):
            try:
                img_data = requests.get(img_url).content
                img_name = os.path.join(page_folder, f'image_{i+1}.jpg')
                with open(img_name, 'wb') as handler:
                    handler.write(img_data)
                print(f"Image {i+1} downloaded: {img_name}")
            except Exception as e:
                print(f"Failed to download image {i+1} from {img_url}. Error: {e}")

if __name__ == "__main__":
    base_url = ''
    for i in range(16, 24):
        url = f'{base_url}{i}/'
        print(f"Scraping images from {url}")
        scrape_images(url, i)
