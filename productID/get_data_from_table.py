from bs4 import BeautifulSoup
import re
import csv
 

def getDataFromTable(content):
    # Split the content into key and value
    key, value = content.split(':', 1)

    # Create a dictionary with the single key-value pair
    data = {key.strip()[1:-1]: value.strip()[1:-1]}

    # Extract HTML content from the data
    html_content = data['htmlContent']
    # print(html_content)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup)

    # Find all rows in the table
    table_rows = soup.find_all('tr')
    # print(table_rows)

    csv_data = []

    for row in table_rows:
        # Find all columns (cells) in the row
        row_columns = row.find_all('td')
 
        if row_columns and len(row_columns) >= 7:  # Ensure there are enough columns
            # Extract content from the 2nd and 7th columns (1st and 6th indexes)
            product = row_columns[0]
            eol_announced = row_columns[1].get_text(strip=True)
            end_of_support = row_columns[6].get_text(strip=True)

            product = str(product)
            product_text_cleaned = re.sub(r'<strong>.*?</strong>', '', product)
            product_text_cleaned = re.sub(r'<sup>.*?</sup>', '', product_text_cleaned)
            product = re.sub(r'<.*?>', '', product_text_cleaned).strip()

            # print(f"Product: {product}")
            # print(f"EOL Announced: {eol_announced}")
            # print(f"End of Support: {end_of_support}")
            # print("---")
            
            # Append the extracted data to the list
            csv_data.append([product, eol_announced, end_of_support])

    # Specify the CSV file path
    csv_file_path = 'extracted_data2.csv'

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_data)  # Write new data rows

    # print(f"New data has been appended to '{csv_file_path}'.")
