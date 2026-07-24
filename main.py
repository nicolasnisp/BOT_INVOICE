import traceback
from db.db_insert_into_logs import db_insert_into_logs
from helper.clean_up_task import clean_up_task
from webpage.webpage_starting_challenge import webpage_starting_challenge
from webpage.webpage_download_invoices import webpage_download_invoices
from webpage.webpage_fetching_data import webpage_fetching_data
from webpage.webpage_next_click import webpage_next_click
from excel.excel_create_sheet import create_sheet
from excel.excel_enter_data import enter_data


module_name = __name__.replace("--", "").split(".")[-1]

def main():
    global module_name
    try:
        db_insert_into_logs("Start_Process","Start Process", module_name)

        clean_up_task()

        web_driver = webpage_starting_challenge()
        if not web_driver:
            raise Exception("Error accessing the page")

        create_sheet()

        for counter in range (1, 4):
            fetching_data = webpage_fetching_data(web_driver)
            webpage_download_invoices(web_driver)
            enter_data(fetching_data)
            webpage_next_click(web_driver)

        clean_up_task()




    except Exception as error:
        description = f"An error occurred: Error: [{error}] | Traceback: [{traceback.format_exc()}]"
        db_insert_into_logs("Error", description, module_name)
    finally:
        db_insert_into_logs("Finish_Process", "The Process has Finished.", module_name)


if __name__ == "__main__":
    main()