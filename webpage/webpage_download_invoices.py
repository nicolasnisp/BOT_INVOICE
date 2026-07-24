import traceback
import os
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from db.db_insert_into_logs import db_insert_into_logs
from helper.read_config import (FILE_PATH)

module_name = __name__.split(".")[-1]
description = status = ""


def webpage_download_invoices(web_driver: webdriver) -> str | bool:
    global description, status
    try:
        db_insert_into_logs("Log", "Starting invoice downloads.", module_name)

        for counter in range(1, 5):
                invoice_btn_xpath = f'//*[@id="tableSandbox"]/tbody/tr[{counter}]/td[4]/a'
                invoice_btn = WebDriverWait(web_driver, 30).until(
                    ec.presence_of_element_located((By.XPATH, invoice_btn_xpath)))

                if invoice_btn:
                    img_url = invoice_btn.get_attribute("href")
                    reponse_url = requests.get(img_url)

                    if reponse_url.status_code == 200:
                        file_name = img_url.split('/')[-1]
                        path = os.path.join(FILE_PATH, file_name)

                        with open(path, 'wb') as path:
                            path.write(reponse_url.content)
                            db_insert_into_logs("Log", "Successfully downloaded invoices.", module_name)

        return True
    except Exception as error:
        db_insert_into_logs("Error", f"An error occurred while downloading invoice: Error: [{error}] "
                                         f"| Traceback: [{traceback.format_exc()}]", module_name)