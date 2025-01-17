# Scrape with Screenshot

A smart web scraper that uses AI to extract structured data from any website section you screenshot. Simply capture a part of a webpage containing repeated information (like product listings, search results, or tables), and the AI will automatically identify and extract the relevant data patterns.

## Features
* AI-powered data extraction from webpage screenshots
* Automatic pattern recognition for similar data elements
* Structured JSON output

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
   