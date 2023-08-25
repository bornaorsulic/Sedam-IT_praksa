import requests
from bs4 import BeautifulSoup
import re


def getAllLinks():
    main_url = 'https://support.juniper.net/support/eol/'

    response = requests.get(main_url).text
    soup = BeautifulSoup(response, "html.parser")
    html_content = soup.prettify()

    # Use regular expression to find content between "selector":"sw-eol-table" and end of file
    pattern = r'"label"\s*:\s*"Product and SKU End of Life Dates & Milestones".*?"items"\s*:\s*(\[[\s\S]*?\])'
    match = re.search(pattern, html_content, re.DOTALL)

    if match:
        extracted_content = match.group(1)[1:-1]

        # Find all URLs using regex
        urls = re.findall(r'"url" : "([^"]+)"', extracted_content)
        urls = ["https://support.juniper.net" + s for s in urls]
        # print(urls)

        # Save the extracted links to a text file
        with open('extracted_links.txt', "w") as file:
            for string in urls:
                file.write(string + "\n")

        # print("Extracted links saved to 'extracted_links.txt'")

    else:
        print("###########################################################################No matching content found.")

