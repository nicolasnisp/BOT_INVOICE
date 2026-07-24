import traceback
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from db.db_insert_into_logs import db_insert_into_logs
from helper.read_config import CHALLENGE_URL

module_name = __name__.split(".")[-1]
description = status = ""

def webpage_starting_challenge() -> bool | webdriver:
    global description, status, module_name
    try:
        db_insert_into_logs("Info","Accessing the challenge URL ", module_name)

        options = Options()
        # options.headless = True
        #options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        web_driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

        db_insert_into_logs("Log", "Opening Challenge web page", module_name)
        web_driver.get(CHALLENGE_URL)

        db_insert_into_logs("Log", "Maximizing Challenge web page", module_name)
        web_driver.maximize_window()

        start_btn_id = "start"
        start_btn = WebDriverWait(web_driver, 30).until(ec.presence_of_element_located((By.ID, start_btn_id)))
        if start_btn:
            db_insert_into_logs("Log", "Challenge successfully started.", module_name)
            return web_driver
        
        else:
            db_insert_into_logs("Log", "Unable to access the page.", module_name)
            raise Exception(description)

    except Exception as error:
        db_insert_into_logs("Error", f"An error occurred while downloading invoice: Error: [{error}] |"
                                     f" Traceback: [{traceback.format_exc()}]", module_name)
    return False