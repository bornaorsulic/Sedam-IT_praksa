from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import PyPDF2


# ova funkcija ce otic na stranicu od hpe-a di se nalaze eos i eol datumi za rutere i switches
# tamo ce naci uredaj MSR3012(to ime proizvoda treba proimijeniti ovisno o uredaju kojeg trazis)
# skinuti ce pdf file u kojem se nalaze trazeni datumi
# treba jos samo napraviti da on uzme datume iz tog pdf-a i da ga outputa
def parsingProductWebsite():
    # Initialize the Selenium WebDriver with Firefox
    driver = webdriver.Firefox()

    # Open the website
    driver.get("https://techlibrary.hpe.com/us/en/networking/products/eos/")

    # Wait for the input field to become visible
    wait = WebDriverWait(driver, 10)
    input_element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[3]/div[2]/ul[2]/li[4]/div[1]/span')))
    input_element.click()

    # select first product in drop down menu of the products
    submit_button = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div[2]/ul[1]/li[2]/div[1]/span')
    submit_button.click()

    # Get the page source after performing actions
    page_source = driver.page_source

    # Initialize BeautifulSoup to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')
    html_content = soup.prettify()

    # Parse the HTML using Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <a> elements with href attributes
    anchor_tags = soup.find_all('a', href=True)

    # Disable SSL certificate verification for this request
    requests.packages.urllib3.disable_warnings()

    # Extract and print the href links
    for anchor_tag in anchor_tags:
        href = anchor_tag['href']
        if "MSR3012" in href:
            base_url = 'https://techlibrary.hpe.com'
            complete_url = urljoin(base_url, href)
            response = requests.get(complete_url)

            # Save the PDF content to a local file
            with open("downloaded_pdf.pdf", "wb") as pdf_file:
                pdf_file.write(response.content)

            # Remember to close the WebDriver when done
            driver.quit()


def main():
    parsingProductWebsite()

    # Open the PDF file in read-binary mode
    with open("downloaded_pdf.pdf", "rb") as pdf_file:
        # Initialize a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Get the total number of pages in the PDF
        num_pages = len(pdf_reader.pages)

        # Initialize an empty string to store the extracted text
        extracted_text = ""

        # Iterate through each page and extract text
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text()

    # Search for the target string and capture text until the end of the string
    target_string = 'End of Sale Date:'
    start_index = extracted_text.find(target_string)
    if start_index != -1:
        captured_text = extracted_text[start_index:]
        print(captured_text)
    else:
        print("Target string not found in the extracted text.")


if __name__ == '__main__':
    main()