from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import netsnmp
import re
import csv


# Huawei
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


# -----------------------------------------
# JUNIPER

# Function to extract content from a specific HTML element on a webpage
def getSoftwareReleaseTableFromLink(url):
    # Fetch the HTML content from the URL
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
    else:
        print("No content saved to the text file (error in get_table.py)")


# Function to remove trailing comma and space from a string
def removeTrailingCommaSpace(input_string):
    if input_string.endswith(' ,'):
        return input_string[:-2]
    return input_string


# Function to extract data from an HTML table and write it to a CSV file
def getSoftwareReleaseDataFromTable(content):
    key, value = content.split(':', 1)
    data = {key.strip()[1:-1]: value.strip()[1:-1]}

    html_content = data['htmlContent']
    soup = BeautifulSoup(html_content, 'html.parser')
    table_rows = soup.find_all('tr')

    csv_data = []

    for row in table_rows:
        row_columns = row.find_all('td')

        if row_columns and len(row_columns) >= 4:
            product_column = row_columns[0]
            end_of_engineering = row_columns[2].get_text(strip=True)
            end_of_support = row_columns[3].get_text(strip=True)

            product_text = str(product_column)
            product_text_cleaned = re.sub(r'<sup>.*?</sup>', '', product_text)
            product = re.sub(r'<.*?>', '', product_text_cleaned).strip()
            product = removeTrailingCommaSpace(product)

            csv_data.append([product, end_of_engineering, end_of_support])

    csv_file_path = 'extracted_data.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Product', 'End of Engineering', 'End of Support'])  # Write header
        csv_writer.writerows(csv_data)  # Write data rows


# Function to retrieve software release version of a network device using SNMP
def getSoftwareReleases(hostname, community, OID):
    oid = netsnmp.Varbind(OID)
    result = netsnmp.snmpget(oid, Version=2, DestHost=hostname, Community=community)

    if not result:
        print("No response (error in get_software_release.py)")

    software = 'Junos OS ' + result[0][24:31].decode()
    
    return software


# Function to compare a given product against data in a CSV file and print its end of support
def compareSoftwareReleasesData(product_to_check):
    csv_filename = 'extracted_data.csv'
    product_found = False

    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            if row['Product'] == product_to_check:
                print(f"End of Support for {product_to_check}: {row['End of Support']}")
                print(f"End of Engineering for {product_to_check}: {row['End of Engineering']}\n")
                product_found = True
                break

    if not product_found:
        print("There is no data in the table for the given product (error in compare_the_data.py).")


# ------------------------------------------------------


def getAllLinks(main_url):
    # Fetch HTML content from the main URL
    response = requests.get(main_url).text
    soup = BeautifulSoup(response, "html.parser")
    html_content = soup.prettify()

    # Use regex to find URLs within the specified content
    pattern = r'"label"\s*:\s*"Product and SKU End of Life Dates & Milestones".*?"items"\s*:\s*(\[[\s\S]*?\])'
    match = re.search(pattern, html_content, re.DOTALL)

    if match:
        extracted_content = match.group(1)[1:-1]
        urls = re.findall(r'"url" : "([^"]+)"', extracted_content)
        urls = ["https://support.juniper.net" + s for s in urls]

        # Save the extracted links to a text file
        with open('extracted_links.txt', "w") as file:
            for string in urls:
                file.write(string + "\n")
    else:
        print("No matching content found.")


def getTableFromLink(url):
    # Fetch HTML content from the provided URL
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    html_content = soup.prettify()

    # Use regex to find content within the specified selector
    pattern = r'"selector":"sw-eol-table".*?(\{.*?\})'
    match = re.search(pattern, html_content, re.DOTALL)

    if match:
        extracted_content = match.group(1)[1:-1]

        # Save the extracted content to a text file
        with open('extracted_content.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(extracted_content)
    else:
        print("No matching content found(error in getTableFromLink function).")


def getDataFromTable(content):
    # Split the content into key and value
    key, value = content.split(':', 1)
    data = {key.strip()[1:-1]: value.strip()[1:-1]}
    html_content = data['htmlContent']

    # Create a BeautifulSoup object to parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    table_rows = soup.find_all('tr')
    csv_data = []

    for row in table_rows:
        row_columns = row.find_all('td')

        if row_columns and len(row_columns) >= 7:  # Ensure there are enough columns
            product = row_columns[0]
            eol_announced = row_columns[1].get_text(strip=True)
            end_of_support = row_columns[6].get_text(strip=True)

            # Clean up product text from unnecessary tags
            product = str(product)
            product_text_cleaned = re.sub(r'<strong>.*?</strong>', '', product)
            product_text_cleaned = re.sub(r'<sup>.*?</sup>', '', product_text_cleaned)
            product = re.sub(r'<.*?>', '', product_text_cleaned).strip()

            csv_data.append([product, eol_announced, end_of_support])

    csv_file_path = 'extracted_data2.csv'
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_data)  # Write new data rows


def getDataID(hostname, community, OIDs):
    ID = []
    for OID in OIDs:
        oid = netsnmp.Varbind(OID)

        # Perform SNMP query
        result = netsnmp.snmpget(oid, Version=2, DestHost=hostname, Community=community)

        # Print the result
        if not result:
            print("No response (error in get_data_id.py)")

        # Extract relevant information based on specific conditions
        if "Juniper" in result[0].decode():
            ID.append(result[0][8:14].decode())
        elif "WLAN" in result[0].decode():
            ID.append(result[0][0:5].decode())
    
    return ID


def compareData(products_to_check):
    csv_filename = 'extracted_data2.csv'

    # Open and read the CSV file
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Iterate through each product to check
        for product_to_check in products_to_check:
            for row in csv_reader:
                if product_to_check in row['Product']:
                    print(f"Product: {product_to_check}")
                    print(f"End of Support: {row['End of Support']}")
                    print(f"EOL Announced: {row['EOL Announced']}")
                    print("\n\n")
                    break


# --------------------------------------


def scrapeHPE():
    return 0


# --------------------------------------


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
    

def juniperMain(host, community):
    Software_release_url = 'https://support.juniper.net/support/eol/software/junos/'
    Product_ID_url = 'https://support.juniper.net/support/eol/'
        
    Software_release_oid = '.1.3.6.1.2.1.25.6.3.1.2.2'
    Product_ID_oids = ['.1.3.6.1.4.1.2636.3.63.1.1.1.2.1.3.59']

    getSoftwareReleaseTableFromLink(Software_release_url)

    with open('extracted_content.txt', 'r', encoding='utf-8') as file:
        table_content = file.read().strip()

    getSoftwareReleaseDataFromTable(table_content)

    result = getSoftwareReleases(host, community, Software_release_oid)
    compareSoftwareReleasesData(result)


    # ------------------------------------------------------------------------------------

        
    getAllLinks(Product_ID_url)

    # Create or overwrite the CSV file
    csv_file_path = 'extracted_data2.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Product', 'EOL Announced', 'End of Support'])

    with open('extracted_links.txt', 'r') as file:
        for line in file:
            getTableFromLink(line.strip())

            # Read the content from the extracted_content.txt file
            with open('extracted_content.txt', 'r', encoding='utf-8') as file:
                table_content = file.read().strip()

            getDataFromTable(table_content)

    result = getDataID(host, community, Product_ID_oids)
    compareData(result)
    

def hpeMain(host, community):
    oid = '.1.3.6.1.2.1.1.1'
    # .1.3.6.1.2.1.47.1.1.1.1.2.1 = STRING: "HPE Series Router MSR3012"
    # .1.3.6.1.2.1.47.1.1.1.1.11.1 = STRING: "CN9BK1Q08C
    # .1.3.6.1.4.1.25506.8.35.18.4.3.1.6.0.0 = STRING: "7.1.059 Release 0306P30"

    oid = netsnmp.Varbind(oid)
    results = netsnmp.snmpwalk(oid, Version=2, DestHost=host, Community=community)
    string_results = []
    for result in results:
        result = result.decode('iso-8859-1')
        string_results.append(result)

    string_results = string_results[0]

    if '10.7.20.3' == host:
        device_model_match = re.search(r'\nHPE\s+(\S+)', string_results)
        if device_model_match:
            device_model = device_model_match.group(1)

        # Extract Software Version using a regular expression
        software_version_match = re.search(r'Software Version\s+(\S+)', string_results)
        if software_version_match:
            software_version = software_version_match.group(1)[:-1]

        # Extract Release Version using a regular expression
        release_version_match = re.search(r'Release\s+(\S+)', string_results)
        if release_version_match:
            release_version = release_version_match.group(1)

        print("Device Model:", device_model)
        print("Software Version:", software_version)
        print("Release Version:", release_version)
    
    elif '10.7.20.18' == host:

        # Extract Device Model and Product ID
        device_model_match = re.match(r'HPE (.+ J\d+)', string_results)
        if device_model_match:
            device_model = 'HPE' + device_model_match.group(1)

        # Extract Software Version
        software_version_match = re.search(r'PT\.([\d\.]+)', string_results)
        if software_version_match:
            software_version = 'PT.' + software_version_match.group(1)

        print("Device Model:", device_model)
        print("Software Version:", software_version)


def main():
    host = input("Input the hostname(IP): ")          # 10.7.20.4  | 10.7.20.1   | 10.7.20.3 | 10.7.20.18
    community = input("Input the community string: ") # HuaweiSNMP | junipersnmp |         hpesnmp
    print("")
    

    if "HuaweiSNMP" == community:
        huaweiMain(host, community)

    elif "junipersnmp" == community:
        juniperMain(host, community)
    
    elif "hpesnmp" == community:
        hpeMain(host, community)




if __name__ == '__main__':
    main()
