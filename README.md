# Scrape with Screenshot

A web scraper that allows you to take a screenshot of a section of a website and scrape the data from it.
It's currently in development and designed to scrape array-like data from websites.
For example, you can take a screenshot of a section of a website that contains a list of products, and the scraper will output a JSON file with the product names, prices, and other relevant information.

## Features
* Take screenshot of section of any website to scrape similar data.
* Strucuted JSON output.

## Usage

### Installation

1. Clone this repository and fill in the necessary API keys in the `.env` file:
   ```bash
   git clone https://github.com/TheRayFitzgerald/scrape-with-screenshot.git
   cd scrape-with-screenshot
   cp .env.example .env
   ```
2. Set your screenshots destination to `./screenshots/` directory in the root of the project (guide: [mac](https://www.macrumors.com/how-to/change-screenshots-folder/) | [windows, i guess?](https://www.xda-developers.com/how-change-screenshots-saved-windows-11/)).
3. Install the dependencies and run the script:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 main.py
    ```
4. A browser window will open, take a screenshot of the section of the website you want to scrape. The script will then scrape the website and output the results to a JSON file. 🎉
   

### Example Queries

* 