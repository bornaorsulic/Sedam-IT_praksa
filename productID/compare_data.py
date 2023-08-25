import csv


def compareData(products_to_check):
    # Read the CSV file
    csv_filename = 'extracted_data2.csv'

    # Open and read the CSV file
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Iterate through each row in the CSV
        for product_to_check in products_to_check:
            for row in csv_reader:
                if product_to_check in row['Product']:
                    print(f"Product: {product_to_check}")
                    print(f"End of Support: {row['End of Support']}")
                    print(f"EOL Announced: {row['EOL Announced']}")
                    print("----------------------")
                    break
                