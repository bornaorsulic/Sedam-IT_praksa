from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import os
from fuzzywuzzy import fuzz


def configure_driver():
    driver = webdriver.Firefox()
    return driver


def ConfrimAndQuery(driver):
    # click Confirm button
    confirm_button = driver.find_element(By.XPATH, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[2]/a")
    confirm_button.click()

    # click the query button
    time.sleep(1)
    query_button = driver.find_element(By.XPATH, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[4]/div[2]/a")
    query_button.click()


def scrapeData(driver, xpath_click):
    br = 0
    k = 0
    while True:
        k += 1
        print(k)
        try:
            time.sleep(1)
            next_page = driver.find_element(By.XPATH, f"/html/body/div[8]/div/div[4]/div[3]/span[4]/a[{k}]")
            next_page.click()
        except:
            # getTableData(driver)
            print("get data")
            br += 1
            if br > 1:
                break

        # getTableData(driver)
        print("get data")


    # Wait for the input field to become visible
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    wait = WebDriverWait(driver, 10)
    input_element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_click)))
    input_element.click()


def getProduct(driver, dropdown_xpath, list_of_Xpaths, first):
    if first == "switch":
        # Wait for the input field to become visible
        wait = WebDriverWait(driver, 10)
        input_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/input")))
        input_element.click()
        input_element.send_keys('.')
    elif first == "router":
        # Wait for the routers button be visible    
        wait = WebDriverWait(driver, 10)
        input_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/ul/li[2]")))
        input_element.click()

    try:
        time.sleep(1)
        submit_button = driver.find_element(By.XPATH, dropdown_xpath + "/span")
    except:
        time.sleep(1)
        submit_button = driver.find_element(By.XPATH, dropdown_xpath)
    submit_button.click()


    for xpath in list_of_Xpaths:
        try:
            time.sleep(1)
            submit_button = driver.find_element(By.XPATH, xpath)
        except:
            time.sleep(1)
            submit_button = driver.find_element(By.XPATH, xpath + "/span")
        submit_button.click()
        try:
            ConfrimAndQuery(driver)
            scrapeData(driver, "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/input")
        except:
            pass


def getTableData(driver):
    # Get the page source after performing actions
    page_source = driver.page_source

    # Initialize BeautifulSoup to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')
    html_content = soup.prettify()

    # Store the parsed HTML content to a text file
    file_path_html = 'C:\\Users\\borna\\OneDrive\\Desktop\\praksaBornaOrsulic\\Huawei\\parsed_html.html'
    with open(file_path_html, "w", encoding="utf-8") as file:
        file.write(html_content)
    file.close()

    # Split the HTML content into individual <ul> blocks
    ul_blocks = html_content.split('<ul class="">')
    ul_blocks2 = html_content.split('<ul class="info-result-even">')
    ul_blocks += ul_blocks2

    # Initialize lists to store the extracted data
    products = []
    eom_dates = []
    eos_dates = []

    # Loop through each <ul> block and parse the HTML content
    for block in ul_blocks[1:]:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(block, 'html.parser')

        # Find the elements for Product, EOM, and EOS
        product_element = soup.find('li', class_='pModel')
        eom_element = soup.find('li', class_='eomIntended')
        eos_element = soup.find('li', class_='eosIntended')

        # Extract and store the data
        if product_element:
            product = product_element.get_text().strip()
            products.append(product)

        if eom_element:
            eom_date = eom_element.get_text().strip()
            eom_dates.append(eom_date)

        if eos_element:
            eos_date = eos_element.get_text().strip()
            eos_dates.append(eos_date)

    # Existing data dictionary to keep track of products already in the CSV
    existing_data = {}

    # Load existing data from the CSV
    with open("Huawei_Data.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            product, eom_date, eos_date = row
            existing_data[product] = (eom_date, eos_date)
    csvfile.close()

    # Add new data to existing_data dictionary while avoiding duplicates
    for i, product in enumerate(products):
        if product not in existing_data and product != "":
            if checkNewValues("Huawei_Data.csv", product):
                print(f"New added data is: {product}, {eom_dates[i]} and {eos_dates[i]}")
                existing_data[product] = (eom_dates[i], eos_dates[i])
            else:
                print(f"Product: {product} has a similarity score less then 40.")
                print(f"Product: {product}, EOM: {eom_dates[i]} and EOS: {eos_dates[i]}")
                break

    # Write the data back to the CSV file
    try:
        file_path = os.path.join(os.getcwd(), "Huawei_Data.csv")
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for product, (eom_date, eos_date) in existing_data.items():
                writer.writerow([product, eom_date, eos_date])
        csvfile.close()
    except:
        print("PermissionError: [Errno 13] Permission denied: .\Huawei_Data.csv")
        time.sleep(1)


def checkNewValues(csv_file_path, new_value):
    # Initialize a list to store the product names and their similarity scores
    product_similarities = []

    # Open the CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract the product name from the CSV row
            product_name = row['Product']

            # Calculate the similarity score between new_value and the product name
            similarity_score = fuzz.ratio(new_value, product_name)

            # Add the product name and similarity score to the list
            product_similarities.append((product_name, similarity_score))
    file.close()

    # Sort the list by similarity score in descending order
    product_similarities.sort(key=lambda x: x[1], reverse=True)

    # Print the top N similar products and their similarity scores
    N = 1  # Change N to control how many results to display
    for i, (product, similarity) in enumerate(product_similarities[:N], start=1):
        print(f"{i}. Product: {product}, Similarity Score: {similarity}")
        if similarity >= 40:
            return True


def parsingProductWebsite():
    # Initialize the Selenium WebDriver with Firefox
    driver = configure_driver()

    driver.get("https://info.support.huawei.com/info-finder/tool/en/enterprise/eom-eofs-and-eos-date/product/")


    list_of_Xpaths_campus_switch = [
        f'/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[{i}]'
        for i in range(1, 13)
    ]
    dropdown_xpath_campus_switch = "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div[1]/ul/li[1]/ul/li[1]"
    
    list_of_Xpaths_center_switch = ['/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[1]',
                                    '/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[2]']
    dropdown_xpath_center_switch = "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div[1]/ul/li[1]/ul/li[2]"
    
    getProduct(driver, dropdown_xpath_campus_switch, list_of_Xpaths_campus_switch, "switch")
    getProduct(driver, dropdown_xpath_center_switch, list_of_Xpaths_center_switch, False)

    list_of_Xpaths_core_router = ["/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li"]
    dropdown_xpath_core_router = "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/ul/li[2]/ul/li[1]"

    list_of_Xpaths_service_router = [
        f"/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[{i}]"
        for i in range(1, 16)
    ]
    dropdown_xpath_service_router = "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/ul/li[2]/ul/li[2]"
    
    list_of_Xpaths_access_router = [
        f"/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[{i}]"
        for i in range(1, 7)
    ]
    dropdown_xpath_access_router = "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/ul/li[2]/ul/li[3]"
    
    list_of_Xpaths_iot_getaway = [
        f"/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[{i}]"
        for i in range(1, 4)
    ]
    dropdown_xpath_iot_getaway = "/html/body/div[8]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/ul/li[2]/ul/li[4]"


    getProduct(driver, dropdown_xpath_core_router, list_of_Xpaths_core_router, "router")
    getProduct(driver, dropdown_xpath_service_router, list_of_Xpaths_service_router, False)
    getProduct(driver, dropdown_xpath_access_router, list_of_Xpaths_access_router, False)
    getProduct(driver, dropdown_xpath_iot_getaway, list_of_Xpaths_iot_getaway, False)


def productSubSeries(driver, subSeries, list_of_models):
    br = 0
    for product in subSeries:
        try:
            time.sleep(1)
            submit_button = driver.find_element(By.XPATH, product + "/span")
            submit_button.click()
        except:
            try:
                time.sleep(1)
                submit_button = driver.find_element(By.XPATH, product)
                submit_button.click()
            except:
                try:
                    if br == 0:
                        time.sleep(1)
                        submit_button = driver.find_element(By.XPATH, product[:-3])
                        submit_button.click()
                        br = 1
                    else:
                        return None
                except:
                    return None
        
        try:
            ConfrimAndQuery(driver)
            scrapeData(driver, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/input")

        except:
            pass

        for model in list_of_models:
            try:
                time.sleep(1)
                submit_button = driver.find_element(By.XPATH, model)
                submit_button.click()
            except:
                try:
                    time.sleep(1)
                    submit_button = driver.find_element(By.XPATH, model + "/span")
                    submit_button.click()
                except:
                    break
                
            try:
                ConfrimAndQuery(driver)
                scrapeData(driver, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/input")
            except:
                pass


def getSoftwareVersion(driver, dropdown_xpath, list_of_Xpaths, list_of_models, subSeries, first):
    if first == "switch":
        # Wait for the input field to become visible
        wait = WebDriverWait(driver, 10)
        input_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/input")))
        input_element.click()
        input_element.send_keys(".")
    elif first == "router":
        # Wait for the routers button be visible    
        wait = WebDriverWait(driver, 10)
        input_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div/ul/li[2]")))
        input_element.click()

    try:
        time.sleep(1)
        submit_button = driver.find_element(By.XPATH, dropdown_xpath)
    except:
        time.sleep(1)
        submit_button = driver.find_element(By.XPATH, dropdown_xpath + "/span")
    submit_button.click()

    for xpath in list_of_Xpaths:
        try:
            time.sleep(1)
            submit_button = driver.find_element(By.XPATH, xpath)
        except:
            time.sleep(1)
            submit_button = driver.find_element(By.XPATH, xpath + "/span")
        submit_button.click()

        try:
            ConfrimAndQuery(driver)
            scrapeData(driver, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/input")
        except:
            for model in list_of_models:
                try:
                    time.sleep(1)
                    submit_button = driver.find_element(By.XPATH, model)
                    submit_button.click()
                    
                except:
                    try:
                        time.sleep(1)
                        submit_button = driver.find_element(By.XPATH, model + "/span")
                        submit_button.click()
                        
                    except:
                        print(1)
                        productSubSeries(driver, subSeries, list_of_models)
                        print(2)
                        break
                
                try:
                    ConfrimAndQuery(driver)
                    scrapeData(driver, "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/input")
                except:
                    pass


def parsingSoftwareVersionWebsite():
    # Initialize the Selenium WebDriver with Firefox
    driver = configure_driver()

    driver.get("https://info.support.huawei.com/info-finder/tool/en/enterprise/eom-eofs-and-eos-date/version")


    dropdown_xpath = "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[1]/ul/li[1]/ul/li[1]"
    list_of_Xpaths = [
        f'/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[{i}]'
        for i in range(4, 13)
    ]
    list_of_models = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[4]/ul/li[{k}]"
        for k in range(1, 40)
    ]
    subSeries = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[3]/ul/li[{j}]"
        for j in range(1, 40)
    ]
    getSoftwareVersion(driver, dropdown_xpath, list_of_Xpaths, list_of_models, subSeries, "switch")

    dropdown_xpath = "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[1]/ul/li[1]/ul/li[2]"
    list_of_Xpaths = [
        f'/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[{i}]'
        for i in range(1, 3)
    ]
    list_of_models = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[4]/ul/li[{k}]"
        for k in range(1, 60)
    ]
    subSeries = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[3]/ul/li[{j}]"
        for j in range(1, 60)
    ]
    getSoftwareVersion(driver, dropdown_xpath, list_of_Xpaths, list_of_models, subSeries, False)

# --------------------
    list_of_Xpaths = ["/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li"]
    dropdown_xpath = "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div/ul/li[2]/ul/li[1]"
    list_of_models=[]
    subSeries=[]
    getSoftwareVersion(driver, dropdown_xpath, list_of_Xpaths, list_of_models, subSeries, "router")
# --------------------
    list_of_Xpaths = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[{i}]"
        for i in range(1, 16)
    ]
    dropdown_xpath = "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[1]/ul/li[2]/ul/li[2]"
    list_of_models = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[3]/ul/li[{k}]"
        for k in range(1, 60)
    ]
    subSeries = []
    getSoftwareVersion(driver, dropdown_xpath, list_of_Xpaths, list_of_models, subSeries, False)
# --------------------
    list_of_Xpaths = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[{i}]"
        for i in range(1, 7)
    ]
    dropdown_xpath = "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[1]/ul/li[2]/ul/li[3]"
    list_of_models = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[4]/ul/li[{k}]"
        for k in range(1, 60)
    ]
    subSeries = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[3]/ul/li[{j}]"
        for j in range(1, 60)
    ]
    getSoftwareVersion(driver, dropdown_xpath, list_of_Xpaths, list_of_models, subSeries, False)
# --------------------
    list_of_Xpaths = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[2]/ul/li[{i}]"
        for i in range(1, 4)
    ]
    dropdown_xpath = "/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[1]/ul/li[2]/ul/li[4]"
    list_of_models = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[4]/ul/li[{k}]"
        for k in range(1, 30)
    ]
    subSeries = [
        f"/html/body/div[8]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[3]/ul/li[{j}]"
        for j in range(1, 5)
    ]
    getSoftwareVersion(driver, dropdown_xpath, list_of_Xpaths, list_of_models, subSeries, False)


# parsingProductWebsite()
parsingSoftwareVersionWebsite()
