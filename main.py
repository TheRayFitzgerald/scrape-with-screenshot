import base64
import time
import os

from inspect import cleandoc
from dotenv import load_dotenv


from anthropic import Anthropic
from openai import OpenAI
from firecrawl import FirecrawlApp

from colorama import Fore, Style, init


FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TEST_RUN_DATA_DIR = "test_run_data"
URL = "https://www.producthunt.com/leaderboard/daily/2024/7/13?ref=header_nav"
ITER = 4

SYSTEM_PROMPT = cleandoc(
    """
    You are an advanced AI model that can extract structured data from large bodies of text.
    You excel in scraping key information from webpages and images.
    You think step by step, and apply nuanced reasoning to extract structured data from unstructured text.
    """
)


init(autoreset=True)
load_dotenv()
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
openai = OpenAI(api_key=OPENAI_API_KEY)


def base64_encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_data_from_image_0(image_path: str) -> str:
    print("!! extract_data_from_image")
    # Getting the base64 string
    base64_image = base64_encode_image(image_path)

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


def extract_data_from_image(image_path: str) -> str:
    print("!! extract_data_from_image")

    base64_image = base64_encode_image(image_path)

    message = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64_image,
                        },
                    },
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
                ],
            },
            {
                "role": "assistant",
                "content": "{",
            },
        ],
    )
    # return message.content[0].text but with the `{` added at the beginning
    return "{" + message.content[0].text


def scrape_url(url: str) -> str:
    print("!! scrape_url")
    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

    try:
        scraped_data = app.scrape_url(url)
    except Exception as e:
        print(f"Unable to scrape the URL: {url}. Error: {e}")
        return "Unable to scrape the URL."
    markdown_data = scraped_data.get("markdown")

    return markdown_data


def extract_full_page_data(image_data: str, page_data: str) -> dict:
    print("!! extract_full_page_data")

    with anthropic.messages.stream(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=SYSTEM_PROMPT,
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
                        - Do **not** extend the JSON format to include additional fields or data.
                    - **You must extract as many sets as possible.**
                      - If you encounter a set of data that is not in the same JSON format as the structured subset data, you can skip it. Keep extracting the next set of data.
                    - If you cannot find any data in the full page data that matches the structured subset data, return an empty object.
                    
                """
                ),
            },
            {
                "role": "assistant",
                "content": "{",
            },
        ],
    ) as stream:
        print(f"{Fore.GREEN}{{", end="")
        for text in stream.text_stream:
            print(
                f"{Fore.GREEN}{text}{Style.RESET_ALL}",
                end="",
                flush=True,
            )


def test_run():
    with open(f"{TEST_RUN_DATA_DIR}/scraped_webpages/{ITER}.txt", "r") as file:
        page_data = file.read()

    with open(f"{TEST_RUN_DATA_DIR}/image_descriptions/{ITER}.txt", "r") as file:
        image_data = file.read()

    extract_full_page_data(image_data, page_data)


def main():
    with open(f"{TEST_RUN_DATA_DIR}/scraped_webpages/{ITER}.txt", "r") as file:
        page_data = file.read()
    while True:
        os.system("rm -rf screenshots/*")
        os.system("mkdir -p screenshots")

        print(
            f"{Fore.RED}\nWaiting for the user to take a screenshot...{Style.RESET_ALL}"
        )
        while True:
            if os.listdir("screenshots"):
                # sleep for 1 second to ensure the image is saved
                time.sleep(1)
                print(f"{Fore.GREEN}Screenshot taken!{Style.RESET_ALL}")
                break

        image_path = os.path.join("screenshots", os.listdir("screenshots")[0])

        image_data_0 = extract_data_from_image_0(image_path)
        print(image_data_0)

        image_data = extract_data_from_image(image_path)
        print(image_data)

        # page_data = scrape_url(URL)
        # extract_full_page_data(image_data, page_data)


if __name__ == "__main__":
    main()
