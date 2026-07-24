import traceback
from time import sleep
import openpyxl
from db.db_insert_into_logs import db_insert_into_logs
from helper.read_config import FILE_PATH, FILE_PATH_SHEET

module_name = __name__.split(".")[-1]

def enter_data(data: list):
    global sheet_page, line
    try:
        db_insert_into_logs("Log", "Starting to insert data.", module_name)

        sheet_file = openpyxl.load_workbook(FILE_PATH_SHEET)
        sheet_page = sheet_file["Info"]
        for row in data:
            line = [row["Numero"], row["Id"], row["data"], row["Invoice"]]
            sheet_page.append(line)


        sheet_file.save(FILE_PATH_SHEET)

        sleep(4)

    except Exception as error:
        db_insert_into_logs(
            "Error",f"Error inserting the header: [{error}] | Traceback: [{traceback.format_exc()}]",
            module_name
        )
