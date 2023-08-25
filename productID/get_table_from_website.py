import requests
from bs4 import BeautifulSoup
import re


def getTableFromLink(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    html_content = soup.prettify()

    # Use regular expression to find content between "selector":"sw-eol-table" and end of file
    pattern = r'"selector":"sw-eol-table".*?(\{.*?\})'
    match = re.search(pattern, html_content, re.DOTALL)

    if match:
        extracted_content = match.group(1)[1:-1]

        # Save the extracted content to a text file
        with open('extracted_content.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(extracted_content)
        # print("Extracted content saved to 'extracted_content.txt'")
    else:
        print("#########################################################33No matching content found.")


