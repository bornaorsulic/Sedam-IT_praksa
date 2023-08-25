import csv


def compareData(product_to_check):
    """
    Compares a given product against data in a CSV file and prints its end of support if found.

    Parameters:
        product_to_check (str): The product name to search for in the CSV file.

    Returns:
        None

    This function reads a CSV file ('extracted_data.csv') containing product information
    and searches for a given product name. If the product is found, it prints the associated
    end of support date. If the product is not found, an error message is printed.
    """
    # Read the CSV file
    csv_filename = 'extracted_data.csv'

    # Initialize a flag to track if the product is found
    product_found = False

    # Open and read the CSV file
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Iterate through each row in the CSV
        for row in csv_reader:
            if row['Product'] == product_to_check:
                print(f"End of Support for {product_to_check}: {row['End of Support']}")
                print(f"End of Engineering for {product_to_check}: {row['End of Engineering']}")
                product_found = True
                break

    # If the product is not found, print the message
    if not product_found:
        print("There is no data in the table for the given product(something wrong in compare_the_data.py).")
