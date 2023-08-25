# Network Device Software and End-of-Life Data Scraper

## Introduction

This Python script is designed to scrape and analyze end-of-support (EOS) and end-of-life (EOL) data from Juniper Networks' support website using web scraping techniques. It extracts information about product versions, EOL dates, EOS dates and engineering end dates. The script also retrieves additional data using SNMP (Simple Network Management Protocol) queries. The extracted data is then processed, compared, and presented to the user.

## Prerequisites

- Python 3.x
- Required Python packages: `requests`, `beautifulsoup4`, `re`, `csv`, `netsnmp`

## Usage

1. **Collecting Software Release and EOL Data**

   The script collects software release and EOL data from Juniper Networks' support website by utilizing web scraping techniques.

   - The function `getSoftwareReleaseTableFromLink(url)` fetches HTML content from a given URL and extracts the software release table content using regular expressions. The extracted content is saved to a text file.

   - The function `removeTrailingCommaSpace(input_string)` removes trailing comma and space characters from a string.

   - The function `getSoftwareReleaseDataFromTable(content)` parses HTML table data extracted from the previous step. It cleans up the data and writes it to a CSV file.

   - The function `getSoftwareReleases(hostname, community, OID)` retrieves software release version information from a network device using SNMP. The SNMP query is performed to fetch Software Release that device is using.

   - The function `compareSoftwareReleasesData(product_to_check)` compares a given product against the data in the CSV file and prints its EOS and engineering end dates if found.


2. **Collecting Product ID Data**

   The script also collects product ID data from Juniper Networks' support website.

   - The function `getAllLinks(main_url)` fetches HTML content from a main URL, extracts URLs for product details, and saves them to a text file.

   - The function `getTableFromLink(url)` fetches HTML content from a URL, extracts table content using regular expressions, and saves it to a text file.

   - The function `getDataFromTable(content)` extracts data from the previously saved table content. It cleans up the data and appends it to a CSV file.

   - The function `getDataID(hostname, community, OIDs)` retrieves specific data IDs from a network device using SNMP. The SNMP query is performed to fetch relevant data IDs based on certain conditions.

   - The function `compareData(products_to_check)` compares specified products against the collected data and prints their EOL announced and end of support dates.

3. **Main Execution**

   The main execution function `main()` orchestrates the entire process.

   - The user is prompted to input the hostname (IP) and community string for SNMP queries.

   - Software release and EOL data are scraped and processed for a network device using the previously defined functions.

   - Product ID data is collected and processed using similar methods.

   - Finally, the script compares the collected data and presents the relevant EOL and engineering end dates to the user.

## How to Run

1.	Install the required Python packages using `pip install`.

2. Run the script in a Python environment.

3. Follow the prompts to input the hostname (for Juniper in Sedam IT is 10.7.20.1) and community string (for Juniper in Sedam IT is junipersnmp) for SNMP queries.

4. The script will perform data collection, processing, and comparison as described above.

## Input and Output

- **Input**: The script prompts the user to input the network device's hostname (IP address) and SNMP community string.

- **Output**: The script outputs various messages indicating the progress of data collection, processing, and comparison. It displays extracted data, comparison results, and relevant dates.

## Known Issues

**Juniper SRX550 Internet Router**: Using SNMP, you can obtain information that the router being used is an SRX550 (.1.3.6.1.4.1.2636.3.1.2.0 = STRING: "Juniper SRX550 Internet Router"). However, the specific model or configuration cannot be determined through SNMP. I even tried connecting to the SRX550 router with SSH but couldn't get the right model. The website states that there is an SRX550-CHAS-M model with associated End of Support (EOS) and End of Life (EOL) dates.


**Web Scraping**: If any changes are made to the website, the web scraping process might no longer function correctly. It's highly likely that the extracted data won't be correctly saved in a CSV file.

## Contact

If you have any questions, suggestions, or feedback about this project, feel free to reach out:

- **Name**: Borna Oršulić
- **GitHub**: [bornaorsulic](https://github.com/bornaorsulic)
- **Email**: borna.orsulic2@gmail.com
