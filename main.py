from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
from datetime import date
from threading import Thread
from time import sleep


URL_ROOT = "https://www.bbc.com"
URL_PATH = "/news"
DRIVER_PATH = "chromedriver.exe"


def ending_process():
    print("Enter 'exit' to end the process...")
    while input() != "exit":
        pass
    print("Ending the process...")


def get_page(driver, page_url):
    driver.get(page_url)
    return BeautifulSoup(driver.page_source, "html.parser")


def search_page(page, function_number):

    # Search Activities
    search = {
        0: page.find_all('a', class_="gs-c-promo-heading"),
        1: page.find("h3", class_="gs-c-promo-heading__title")
    }
    return search[function_number]


def open_file(name):
    filename = name + date.today().strftime("%d-%m-%Y") + ".csv"
    file = open(filename, mode="a+", encoding="utf-8")
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    records = list(csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL))

    return file, writer, records


def get_article_info(parent, child):
    global URL_ROOT

    article_title = child.text
    href_link = parent.get("href")

    # Making sure the link contains the url root
    if href_link[:len(URL_ROOT) - 1] == URL_ROOT:
        article_href = parent.get("href")
    else:
        article_href = URL_ROOT + parent.get("href")

    return [article_title, article_href]


def extract_info(page, records, writer):
    parents = search_page(page, 0)
    for parent in parents:
        child = search_page(parent, 1)
        if child is not None:

            # Extracting useful information
            data = get_article_info(parent, child)

            # Adding in the unique information
            if data not in records:
                records.append(data)
                print("Article: ", data[0])
                print("Address: ", data[1])
                writer.writerow(data)

    return records


def extraction_process(driver):
    global URL_ROOT
    global URL_PATH

    # Creating a thread
    thread = Thread(target=ending_process)
    thread.start()

    # File Handling
    file, writer, records = open_file("information_")
    while thread.is_alive():

        # Getting info
        page = get_page(driver, URL_ROOT + URL_PATH)
        records = extract_info(page, records, writer)

        # Simulating interrupts
        counter = 0
        while thread.is_alive():
            sleep(5)
            counter += 1
            if counter == 60:
                break
    file.close()
    print("Process ended.")


def web_scrap():
    global DRIVER_PATH

    # Creating the drivers
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(DRIVER_PATH, options=options)

    extraction_process(driver)


web_scrap()
