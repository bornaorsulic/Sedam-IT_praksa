from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import netsnmp
import re


def configure_driver():
    options = webdriver.FirefoxOptions()
    options.headless = True  # Set headless mode
    driver = webdriver.Firefox(options=options)
    return driver


def parsingProductWebsite(product):
    # Initialize the Selenium WebDriver with Firefox
    driver = configure_driver()

    driver.get("https://info.support.huawei.com/info-finder/tool/en/enterprise/eom-eofs-and-eos-date/product/")

    # Wait for the input field to become visible
    wait = WebDriverWait(driver, 10)
    input_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/input")))
    input_element.click()
    input_element.send_keys(product)

    # select first product in drop down menu of the products
    submit_button = driver.find_element(By.XPATH, "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/ul/li[1]")
    submit_button.click()

    # Submit the form or perform any necessary actions
    submit_button = driver.find_element(By.XPATH, "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[3]/div[2]/a")
    submit_button.click()

    # Get the page source after performing actions
    page_source = driver.page_source

    # Initialize BeautifulSoup to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')
    html_content = soup.prettify()

    # Store the parsed HTML content to a text file
    with open("parsed_html.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    # Remember to close the WebDriver when done
    driver.quit()


def getProductDates(product):
    # Read the HTML content from the file and store it as a string
    with open('parsed_html.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Find the starting index of the first <ul class=""> occurrence
    extracted_content = html_content.split('<ul class="">')
    extracted_content = extracted_content[1].split('</ul>')

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(extracted_content[0], 'html.parser')

    # Find the elements for EOM and EOS
    eom_element = soup.find('li', class_='eomIntended')
    eos_element = soup.find('li', class_='eosIntended')

    print(f"Product: {product}")
    # Extract and print the dates for EOM and EOS
    if eom_element:
        eom_date = eom_element.get_text().strip()
        print("End of Marketing (EOM) Date:", eom_date)
    else:
        print("There is no Marketing (EOM) Date!!")

    if eos_element:
        eos_date = eos_element.get_text().strip()
        print("End of Service (EOS) Date:", eos_date)
    else:
        print("There is no Service (EOS) Date!!")


def parsingSoftwareVersionWebsite(product):
    # Initialize the Selenium WebDriver with Firefox
    driver = configure_driver()

    driver.get("https://info.support.huawei.com/info-finder/tool/en/enterprise/eom-eofs-and-eos-date/version")

    # Wait for the input field to become visible
    wait = WebDriverWait(driver, 10)
    input_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/input")))
    input_element.click()
    input_element.send_keys(product)

    # select first product in drop down menu of the products
    submit_button = driver.find_element(By.XPATH, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/ul/li")
    submit_button.click()

    # Submit the form or perform any necessary actions
    submit_button = driver.find_element(By.XPATH, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[4]/div[2]/a")
    submit_button.click()

    # Get the page source after performing actions
    page_source = driver.page_source

    # Initialize BeautifulSoup to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')
    html_content = soup.prettify()

    # Store the parsed HTML content to a text file
    with open("parsed_html.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    # Remember to close the WebDriver when done
    driver.quit()


def extract_product_info(li_element):
    class_name = li_element.get('class')[0]
    text = li_element.get_text(strip=True)
    info_mapping = {
        'pModel': 'Product Version',
        'eosIntended': 'End of Service (EOS)',
        'eomIntended': 'End of Marketing (EOM)',
        'eofsIntended': 'End of Full Support (EOFS)'
    }
    return info_mapping.get(class_name, ''), text


def get_cleaned_content(extracted_content):
    start_index = extracted_content.find('<ul class="tr-template">')
    end_index = extracted_content.find('</ul>', start_index)
    before_block = extracted_content[:start_index]
    after_block = extracted_content[end_index + len('</ul>'):]
    return before_block + after_block


def get_product_data(version, soup):
    ul_elements = soup.find_all('ul', class_='info-result-even') + soup.find_all('ul', class_='')

    for ul_element in ul_elements:
        product_info = {}
        li_elements = ul_element.find_all('li')

        for li_element in li_elements:
            field_name, field_value = extract_product_info(li_element)
            if field_name:
                product_info[field_name] = field_value

        if product_info:
            if product_info['Product Version'] == version:
                return product_info

    print("No version found in the table!!")


def getSoftwareVersionDates(version):
    with open('parsed_html.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Extract specific content from the HTML
    extracted_content = html_content.split('<div class="info-result-tr">')[1].split('</div>')[0]
    cleaned_content = get_cleaned_content(extracted_content)
    soup = BeautifulSoup(cleaned_content, 'html.parser')
    product_data = get_product_data(version, soup)

    for key, value in product_data.items():
        print(f"{key}: {value}")


def huaweiMain(host, community):
    oid = '.1.3.6.1.2.1.1.1.0'
    oid = netsnmp.Varbind(oid)
    result = netsnmp.snmpget(oid, Version=2, DestHost=host, Community=community)
    result = result[0].decode()

    # Extract the model (second word)
    product = result.split()[1]

    # Extract the version (second word in the bracket)
    version_match = re.search(r'\((\w+ \w+)\)', result)
    version = version_match.group(1) if version_match else None
    version = version.split()[1][:-6]

    parsingProductWebsite(product)
    getProductDates(product)  # Core Routers are not working

    parsingSoftwareVersionWebsite(product)
    getSoftwareVersionDates(version)

    
def main():
    host = input("Input the IP: ") # 10.7.20.4
    community = input("Input the community string: ") # HuaweiSNMP
    print("")
    
    if "HuaweiSNMP" == community:
        huaweiMain(host, community)


if __name__ == '__main__':
    main()
