from bs4 import BeautifulSoup
import re
import csv


def removeTrailingCommaSpace(input_string):
    """
    Removes a trailing comma and space from the given input string.

    Parameters:
        input_string (str): The string to be processed.

    Returns:
        str: The processed string with trailing comma and space removed if present.
    """
    if input_string.endswith(' ,'):
        return input_string[:-2]
    return input_string


def getDataFromTable(content):
    """
    Extracts data from an HTML table content and writes it to a CSV file.

    Parameters:
        content (str): The HTML content containing the table.

    Returns:
        None

    This function takes an HTML content as input, extracts data from a specific table structure,
    and writes the extracted data (product names and end of support dates) to a CSV file.
    It uses Beautiful Soup to parse the HTML content and extract table rows and columns.
    """
    # Split the content into key and value
    key, value = content.split(':', 1)

    # Create a dictionary with the single key-value pair
    data = {key.strip()[1:-1]: value.strip()[1:-1]}

    # Extract HTML content from the data
    html_content = data['htmlContent']

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all rows in the table
    table_rows = soup.find_all('tr')

    csv_data = []

    for row in table_rows:
        # Find all columns (cells) in the row
        row_columns = row.find_all('td')

        if row_columns and len(row_columns) >= 4:

            # Extract content from the 1st and 4th columns (0th and 3rd indexes)
            product_column = row_columns[0]
            end_of_engineering = row_columns[2].get_text(strip=True)
            end_of_support = row_columns[3].get_text(strip=True)

            # Remove <sup> tags and their content in the product column
            product_text = str(product_column)
            product_text_cleaned = re.sub(r'<sup>.*?</sup>', '', product_text)
            product = re.sub(r'<.*?>', '', product_text_cleaned).strip()
            product = removeTrailingCommaSpace(product)

            # print(f"Product: {product}")
            # print(f"End of Support: {end_of_support}")
            # print("---")

            # Append the extracted data to the list
            csv_data.append([product, end_of_engineering, end_of_support])

    # Specify the CSV file path
    csv_file_path = 'extracted_data.csv'

    # Write the data to a CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Product', 'End of Engineering', 'End of Support'])  # Write header
        csv_writer.writerows(csv_data)  # Write data rows

    print(f"Data has been saved to '{csv_file_path}'.")
