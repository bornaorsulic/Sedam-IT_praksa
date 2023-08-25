import requests
from bs4 import BeautifulSoup
import re
import csv
import netsnmp


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
        print("Extracted content saved to 'extracted_content.txt'")
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

    print(f"Data has been saved to '{csv_file_path}'.")


# Function to retrieve software release version of a network device using SNMP
def getSoftwareReleases(hostname, community, OID):
    oid = netsnmp.Varbind(OID)
    result = netsnmp.snmpget(oid, Version=2, DestHost=hostname, Community=community)

    if not result:
        print("No response (error in get_software_release.py)")
    else:
        print(OID, " -> ", result[0].decode())

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
                print("|-----------------------------------------------------|")
                print(f"|End of Support for {product_to_check}: {row['End of Support']}      |")
                print(f"|End of Engineering for {product_to_check}: {row['End of Engineering']}  |")
                print("|-----------------------------------------------------|\n\n")
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
        # print("Extracted content saved to 'extracted_content.txt'")
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
        else:
            print(OID, " -> ", result[0].decode())

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
                    print("|-----------------------------------------------------|")
                    print(f"|Product: {product_to_check}                                       |")
                    print(f"|End of Support: {row['End of Support']}                           |")
                    print(f"|EOL Announced: {row['EOL Announced']}                            |")
                    print("|-----------------------------------------------------|\n\n")
                    break


def main():
    Software_release_url = 'https://support.juniper.net/support/eol/software/junos/'
    Product_ID_url = 'https://support.juniper.net/support/eol/'
    
    Software_release_oid = '.1.3.6.1.2.1.25.6.3.1.2.2'
    Product_ID_oids = ['.1.3.6.1.4.1.2636.3.63.1.1.1.2.1.3.59']

    hostname = input("Input hostname(IP): ")
    community = input("Input community string: ")

    getSoftwareReleaseTableFromLink(Software_release_url)

    with open('extracted_content.txt', 'r', encoding='utf-8') as file:
        table_content = file.read().strip()

    getSoftwareReleaseDataFromTable(table_content)

    result = getSoftwareReleases(hostname, community, Software_release_oid)
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

    result = getDataID(hostname, community, Product_ID_oids)
    compareData(result)


if __name__ == '__main__':
    main()

    # .1.3.6.1.4.1.2636.3.1.2.0 = STRING: "Juniper SRX550 Internet Router"
    # .1.3.6.1.4.1.2636.3.63.1.1.1.2.1.3.59 = STRING: "AX411 WLAN AP"
    # https://support.juniper.net/support/eol/product/srx_series/