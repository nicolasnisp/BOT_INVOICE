import traceback
from psutil import process_iter
from AppOpener import close
from db.db_insert_into_logs import db_insert_into_logs

module_name = __name__.split(".")[-1]
description = status = ""

def clean_up_task():
    global description, status, module_name
    try:
        db_insert_into_logs("Log","Closing all process", module_name)

        msedge_flag = False

        for process in process_iter():
            if process.name() == "msedge.exe":
                msedge_flag = True

        if msedge_flag:
            db_insert_into_logs("Log","Closing Microsoft Edge process", module_name)
            close("msedge", output=False)

        for process in process_iter():
            if process.name() =="msedge.exe":
                msedge_flag = False

        if not msedge_flag:
            db_insert_into_logs("Info", "Closing Microsoft Edge process.", module_name)

    except Exception as error:
        db_insert_into_logs("Error",f"An error occurred: Error: [{error}] | Traceback:"
                                    f" [{traceback.format_exc()}] ", module_name)
