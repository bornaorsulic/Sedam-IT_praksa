from open_all_links import getAllLinks
from get_table_from_website import getTableFromLink
from get_data_from_table import getDataFromTable
from get_data_id import getDataID
import compare_data
import csv


def main():
    
    hostname = '10.7.20.1'
    community = 'junipersnmp'
    """
    hostname = input("Input hostname(IP): ")
    community = input("Input community string: ")
    """

    getAllLinks()

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


    result = getDataID(hostname, community)
    compare_data.compareData(result)


if __name__ == '__main__':
    main()
