import requests
from bs4 import BeautifulSoup
import re


def getTableFromLink(url):
    """
    Extracts content from a specific HTML element on a webpage and saves it to a text file.

    Parameters:
        url (str): The URL of the webpage containing the HTML content.

    Returns:
        None

    This function fetches the HTML content from the given URL, searches for a specific HTML element
    with the selector "sw-eol-table", and extracts its content. The extracted content is then saved
    to a text file named 'extracted_content.txt'. If the element is not found, an error message is printed.
    """
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    html_content = soup.prettify()

    # Use regular expression to find content between "selector":"sw-eol-table" and end of file
    pattern = r'"selector":"sw-eol-table".*?(\{.*?\})'
    match = re.search(pattern, html_content, re.DOTALL)

    if match:
        extracted_content = match.group(1)[1:-1]

        # Save the content to a text file
        with open('extracted_content.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(extracted_content)
        print("Extracted content saved to 'extracted_content.txt'")
    else:
        print("No content saved to the text file(error in the get_table.py)")
