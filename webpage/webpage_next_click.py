import traceback
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from db.db_insert_into_logs import db_insert_into_logs

module_name = __name__.split(".")[-1]
description = status = ""

def webpage_next_click(web_driver: webdriver) -> str | bool:

    try:
        db_insert_into_logs("Log", "looking for the next button.", module_name)

        next_btn_xpath = '/html/body/div/div/div[2]/div/div[1]/div[1]/div/a[2]'
        next_btn = WebDriverWait(web_driver, 30).until(ec.presence_of_element_located((By.XPATH, next_btn_xpath)))
        next_btn.click()
        db_insert_into_logs("Log", "Next button successfully found and clicked.", module_name)

    except Exception as error:
        db_insert_into_logs("Error", f"An error occurred upon clicking: Error: [{error}] "
                                         f"| Traceback: [{traceback.format_exc()}]", module_name)