import traceback
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from db.db_insert_into_logs import db_insert_into_logs

module_name = __name__.split(".")[-1]
description = status = ""


def webpage_fetching_data(web_driver: webdriver):
    global invoice_link
    try:
        db_insert_into_logs("Log", "Starting to fetch data.", module_name)
        data = [] #lista de dados

        rows_xpath = f'//*[@id="tableSandbox"]/tbody/tr'
        rows = WebDriverWait(web_driver, 30).until(ec.presence_of_all_elements_located((By.XPATH, rows_xpath)))

        for row in rows:
            element = row.find_elements(By.XPATH, 'td')

            link_tag = element[3].find_elements(By.TAG_NAME, "a")
            if link_tag:
                invoice_link = link_tag[0].get_attribute("href")

            table_data ={  # dicionario
            "Numero": element[0].text,
            "Id": element[1].text,
            "data": element[2].text,
            "Invoice": invoice_link
            }
            data.append(table_data)

        for table_data in data:
            print(table_data)

        return data

    except Exception as error:
        db_insert_into_logs(
            "Error",f"Error the fetch dates: [{error}] | Traceback: [{traceback.format_exc()}]",
            module_name)
        return []