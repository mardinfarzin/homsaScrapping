
# Web Image Downloader

This is a Python-based application that allows users to scrape and download images from a list of URLs, specifically designed for web scraping from the **Hoomsa** website. It uses the BeautifulSoup library to parse HTML content and the Requests library to fetch images.

## Features
- Scrape the listing name from each URL and save it to a text file.
- Download images from a carousel section on the webpage.
- Multi-threaded processing to download images from multiple URLs simultaneously.
- Simple Tkinter-based GUI for user interaction.
- Specifically built for scraping data from the **Hoomsa** website.

## Requirements
- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `tkinter` (should be included with standard Python installations)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/web-image-downloader.git
   ```
2. Install the required libraries:
   ```bash
   pip install requests beautifulsoup4
   ```

## Usage

1. Run the application:
   ```bash
   python download.py
   ```
2. In the Tkinter window, enter one or more URLs (one URL per line). The URLs should be from the **Hoomsa** website.
3. Click the "Download" button to start scraping and downloading images.
4. The images will be saved in directories named `folder_1`, `folder_2`, etc., with each folder containing the listing name and images.

## Notes
- The program specifically scrapes information from the **Hoomsa** website and expects a particular HTML structure (with elements like `#listing_name_wrap`, `#roomMainInfo`, and `#carousel1`). If the structure changes on other pages or websites, it may not work correctly.
- Errors such as connection timeouts or missing elements will be logged in the status area of the GUI.
- The images are saved in `.jpg` format in separate folders for each URL processed.
