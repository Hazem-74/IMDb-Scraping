# IMDb Scraping Project

## Table of Contents
- [Project Overview](#project-overview)
- [Files Description](#files-description)
  - [`Scraping.py`](#scrapingpy)
  - [`image.py`](#imagepy)
  - [`Renaming.py`](#renamingpy)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Configuring Paths and URLs](#configuring-paths-and-urls)
  - [Running the Scripts](#running-the-scripts)
- [Directory Structure](#directory-structure)

## Project Overview
This repository contains a collection of Python scripts designed for web scraping tasks, primarily focusing on extracting movie data from IMDb and processing images. The core script (`Scraping.py`) gathers detailed information about the IMDb Top 250 movies, while the other scripts (`image.py` and `Renaming.py`) provide utilities for general image scraping and organization.

## Files Description

### `Scraping.py`
This script is the main component for scraping IMDb movie data.
- **Purpose**: To extract comprehensive information about the IMDb Top 250 movies, including name, certificate, release year, rating, votes, IMDb link, genres, plot summary, directors, writers, actors, and storyline.
- **Methods**:
    - Utilizes **Selenium WebDriver** (specifically for Chrome) to navigate to the IMDb Top 250 page, handle dynamic content loading (by scrolling down), and extract the initial page source after all elements have loaded.
    - Parses the page source using **BeautifulSoup** to locate an embedded JSON script tag containing structured data about the movies.
    - Extracts primary movie details (Name, Certificate, Year, Rate, Votes, Link, Genres, Plot) from the parsed JSON data.
    - Iterates through individual movie links using **`requests`** and **BeautifulSoup** to perform additional scraping for details like Directors, Writers, Actors, and Storyline, which are not readily available in the initial JSON payload.
    - Employs user-agent headers to mimic a browser request.
- **Main Logic**:
    1.  Initialize Selenium WebDriver and navigate to the IMDb Top 250 page.
    2.  Simulate user scrolling to ensure all dynamic content loads.
    3.  Extract and parse the primary movie data from an embedded JSON script.
    4.  For each movie, visit its individual page to scrape supplementary details.
    5.  Consolidate all extracted data into a Pandas DataFrame.
    6.  Save the DataFrame to a CSV file named `IMDb_Top_Movies.csv`.

### `image.py`
This script is designed for general image scraping from web pages.
- **Purpose**: To download images from a specified range of URLs, organizing them into subfolders based on page numbers.
- **Methods**:
    - Uses **`requests`** to send HTTP GET requests to target URLs.
    - Parses HTML content using **BeautifulSoup** to find anchor (`<a>`) tags with `href` attributes ending in `.jpg/`.
    - Downloads image data and saves each image to a designated folder structure.
    - Implements user-agent headers for robust web requests.
- **Main Logic**:
    1.  Creates a main output folder (`scraped_images3`) and subfolders for each page (e.g., `page_16`, `page_17`).
    2.  Sends a GET request to the provided URL.
    3.  Parses the HTML to find all `<a>` tags where the `href` attribute is a JPEG image URL.
    4.  Downloads each identified image and saves it to the respective page subfolder with a sequential name (e.g., `image_1.jpg`).
- **Note**: The `base_url` variable in the `if __name__ == "__main__":` block is currently empty (`''`) and ***must be configured by the user*** to specify the target website for image scraping. The script iterates through page numbers 16 to 23.

### `Renaming.py`
This script provides utilities for organizing and renaming image files.
- **Purpose**: To consolidate images from multiple subfolders into a single new folder and rename them sequentially.
- **Methods**:
    - Utilizes the `os` module for file system operations (listing directories, creating folders, path manipulation).
    - Uses the `shutil` module for copying files.
- **Main Logic**:
    1.  Creates a new destination folder if it doesn't exist.
    2.  Scans a specified `root_folder` for subfolders.
    3.  Iterates through each subfolder and lists all image files within it.
    4.  Assigns a new sequential numerical name to each image (starting from `1100` by default).
    5.  Copies each image from its original location to the new destination folder with its new name.
- **Note**: The `root_folder` and `new_folder` variables are hardcoded (`'New folder'` and `'newfolder2'`) and ***must be configured by the user*** to match the desired input and output directories.

## Requirements
To run these scripts, you will need:
-   Python 3.7+
-   The following Python libraries:
    -   `selenium`
    -   `beautifulsoup4`
    -   `requests`
    -   `pandas`
-   A web browser (e.g., Google Chrome) and its corresponding WebDriver (e.g., `chromedriver`).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Hazem-74/IMDb-Scraping.git
    cd IMDb-Scraping
    ```

2.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Python dependencies**:
    ```bash
    pip install selenium beautifulsoup4 requests pandas
    ```

4.  **Download ChromeDriver**:
    -   Download the appropriate `chromedriver` version that matches your Chrome browser from [Chromium Downloads](https://chromedriver.chromium.org/downloads).
    -   Place the `chromedriver.exe` (or `chromedriver` on Linux/macOS) in a known location. It's recommended to place it within your project directory or in your system's PATH.
    -   **Important**: You will need to update the `executable_path` variable in `Scraping.py` to point to the correct path of your downloaded `chromedriver`.
        ```python
        # In Scraping.py, modify this line:
        service = Service(executable_path= "C:/Users/Hazem/Downloads/chromedriver.exe") # <-- UPDATE THIS PATH
        ```

## Usage

### Configuring Paths and URLs
Before running, please configure the following variables in the respective scripts:

-   **`Scraping.py`**:
    -   `service = Service(executable_path="YOUR_CHROMEDRIVER_PATH")`: Update `YOUR_CHROMEDRIVER_PATH` to the actual path of your `chromedriver`.

-   **`image.py`**:
    -   `base_url = ''`: This variable is currently empty. You ***must*** define `base_url` to the root URL you intend to scrape images from. For example, `base_url = 'https://example.com/images/'`. The script will then append page numbers (16-23) to this `base_url`.

-   **`Renaming.py`**:
    -   `root_folder = 'New folder'`: Update `'New folder'` to the path of the directory containing the subfolders with images you want to rename and move.
    -   `new_folder = 'newfolder2'`: Update `'newfolder2'` to the desired path for the new folder where all renamed images will be consolidated.

### Running the Scripts
These scripts can be executed directly from your terminal as Python scripts.

1.  **Run `Scraping.py`**:
    ```bash
    python Scraping.py
    ```
    This will launch a Chrome browser, scrape the IMDb Top 250 movies, and save the data to `IMDb_Top_Movies.csv` in the project root directory.

2.  **Run `image.py`**:
    *(Remember to configure `base_url` before running)*
    ```bash
    python image.py
    ```
    This will scrape images from the configured URLs and save them into a `scraped_images3` folder with subfolders for each page.

3.  **Run `Renaming.py`**:
    *(Remember to configure `root_folder` and `new_folder` before running)*
    ```bash
    python Renaming.py
    ```
    This will process images from the specified `root_folder`, rename them sequentially, and move them to the `new_folder`.

**Note on Jupyter Notebooks**: While these files are provided as `.py` scripts, they can be opened and executed cell-by-cell within a Jupyter Notebook environment if you prefer an `interactive workflow`. Simply launch Jupyter Notebook (`jupyter notebook` in your terminal) and then open these `.py` files, or convert them to `.ipynb` files.

## Directory Structure
The expected minimal directory structure for the project:
```
IMDb-Scraping/
├── Scraping.py
├── image.py
├── Renaming.py
└── (your_chromedriver_executable)
```
After running `Scraping.py`:
```
IMDb-Scraping/
├── IMDb_Top_Movies.csv  <-- Output CSV
├── Scraping.py
...
```
After running `image.py`:
```
IMDb-Scraping/
├── scraped_images3/     <-- Output folder for images
│   ├── page_16/
│   │   ├── image_1.jpg
│   │   └── ...
│   ├── page_17/
│   │   ├── image_1.jpg
│   │   └── ...
│   └── ...
├── image.py
...
```
After running `Renaming.py` (assuming `root_folder` was `scraped_images3` and `new_folder` was `final_images` for example):
```
IMDb-Scraping/
├── final_images/        <-- Output folder for renamed images
│   ├── 1100.jpg
│   ├── 1101.jpg
│   └── ...
├── Renaming.py
...
```
