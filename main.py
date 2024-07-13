import base64
from dotenv import load_dotenv
import os
from inspect import cleandoc

from openai import OpenAI
from anthropic import Anthropic
from firecrawl import FirecrawlApp


load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

URL = "https://www.producthunt.com/leaderboard/daily/2024/7/13?ref=header_nav"
ITER = 4

SYSTEM_PROMPT = cleandoc(
    """
    You are an advanced AI model that can extract structured data from large bodies of text.
    You think step by step, and apply nuanced reasoning to extract structured data from unstructured text.
    """
)


def create_extraction_prompt(image_data: str, page_data: str):
    prompt = (
        cleandoc(
            f"""
                    Given the following extracted structured object from a webpage:
                    
                    <structured-subset-data>
                    {image_data}
                    </structured-subset-data>
                    
                    and the following unstructured markdown data containing the full webpage data:
                    
                    <full-page-data>
                    {page_data}
                    </full-page-data>
                    
                    
                    Your job is to identify the structured object in the full page data.
                    You must then identify all the other data in the full page data that shares approximately the same structure as the structured subset data.
                    You must then extract all of the other sets of data that share the similar structure as the structured subset data.
                    
                    Rules for extraction:
                    - Ignore slight variations in the structure, such as special assets or supporting components.
                        - Focus mainly on the main data structure, such as the main content or main components.
                    - You must extract the data in the same JSON format as the structured subset data.
                    - **You must extract as many sets as possible.**
                      - If you encounter a set of data that is not in the same JSON format as the structured subset data, you can skip it. Keep extracting the next set of data.
                    - If you cannot find any data in the full page data that matches the structured subset data, return an empty object.
                    
                """
        ),
    )
    return prompt[0]


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_data_from_image(image_path: str) -> str:
    print("!! extract_data_from_image")
    # Getting the base64 string
    base64_image = encode_image(image_path)

    response = openai.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": cleandoc(
                            """
                            Yyou are an expert web scraper from visual images.
                            Look at this image, extract the key information into a structured JSON format.
                            Infer what are the appropriate fields and data types.
                            Ensure that the JSON format is structured, easy to understand, and follows best practices.
                            """
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    print(response.choices[0].message.content)

    return response.choices[0].message.content


def scrape_url(url: str) -> str:
    print("!! scrape_url")
    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

    try:
        scraped_data = app.scrape_url(url)
    except Exception as e:
        print(f"Unable to scrape the URL: {url}. Error: {e}")
        return "Unable to scrape the URL."
    markdown_data = scraped_data.get("markdown")
    print(markdown_data)
    return markdown_data


def extract_full_page_data(image_data: str, page_data: str) -> dict:
    print("!! extract_full_page_data")
    response = openai.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": cleandoc(
                    f"""
                    Given the following extracted structured object from a webpage:
                    
                    <structured-subset-data>
                    {image_data}
                    </structured-subset-data>
                    
                    and the following unstructured markdown data containing the full webpage data:
                    
                    <full-page-data>
                    {page_data}
                    </full-page-data>
                    
                    
                    Your job is to identify the structured object in the full page data.
                    You must then identify all the other data in the full page data that shares approximately the same structure as the structured subset data.
                    You must then extract all of the other sets of data that share the similar structure as the structured subset data.
                    
                    Rules for extraction:
                    - Ignore slight variations in the structure, such as special assets or supporting components.
                        - Focus mainly on the main data structure, such as the main content or main components.
                    - You must extract the data in the same JSON format as the structured subset data.
                    - **You must extract as many sets as possible.**
                    - If you cannot find any data in the full page data that matches the structured subset data, return an empty object.
                    
                """
                ),
            },
        ],
    )
    print(response.choices[0].message.content)

    return response.choices[0].message.content


def extract_full_page_data_anthropic(image_data: str, page_data: str) -> dict:
    print("!! extract_full_page_data_anthropic")
    message = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": create_extraction_prompt(image_data, page_data),
            },
        ],
    )
    print(message.content[0].text)


if __name__ == "__main__":
    """
    image_path = "screenshots/4.png"
    image_data = extract_data_from_image(image_path)
    print(image_data)
    # url = "https://www.freelancer.com/jobs/artificial-intelligence"
    page_data = scrape_url(URL)
    print(page_data)
    # exit the program
    exit()
    """
    # read image_data from `scraped_webpage.md`
    with open(f"./scraped_webpages/{ITER}.txt", "r") as file:
        page_data = file.read()

    # read page_data from `image_description.txt`
    with open(f"./image_descriptions/{ITER}.txt", "r") as file:
        image_data = file.read()

    print(image_data)
    print()
    print(page_data)
    # full_extracted_data = extract_full_page_data(image_data, page_data)
    extract_full_page_data_anthropic(image_data, page_data)
