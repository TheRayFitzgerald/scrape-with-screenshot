
# Visual Web Scraper

An *visual* web scraper built using the GPT-4 Vision, Claude 3.5 Sonnet, 
[Firecrawl](https://www.firecrawl.dev/), and Selenium.
## Features
* Take screenshot of section of any website to scrape similar data.
* Strucuted JSON output.

## Usage

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

Don't forget to add your `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `FIRECRAWL_API_KEY` to a `.env` file.

### Example Queries

* Get all the relevant details about the team members working at Intercom (https://www.intercom.com/about). Write the results to a CSV file.
* "What are the first 5 posts listed on the hacker news site for today? Write the results to a JSON file."
* How many times is Nvidia mentioned in this article https://finance.yahoo.com/news/nvidia-stock-rises-after-10-for-1-stock-split-204412528.html ? Cite the instances where it is mentioned.
