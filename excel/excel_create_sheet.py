import traceback
import openpyxl
from time import sleep
from db.db_insert_into_logs import db_insert_into_logs
from helper.read_config import (FILE_PATH_SHEET)

module_name = __name__.split(".")[-1]
description = status = ""


def create_sheet():
    try:
        db_insert_into_logs("Log", "Starting to create the Workbook and sheet", module_name)

        sheet_file = openpyxl.Workbook()
        default_sheet = sheet_file.active
        sheet_file.remove(default_sheet)
        sheet_file.create_sheet("Info")
        sheet_page = sheet_file["Info"]
        sheet_page.append(['#', 'Id', 'Due Date', 'Invoice Path'])

        sheet_file.save(FILE_PATH_SHEET)

        sleep(2)
        return True

    except Exception as error:
        db_insert_into_logs(
            "Error",f"Error the fetch dates: [{error}] | Traceback: [{traceback.format_exc()}]",module_name)