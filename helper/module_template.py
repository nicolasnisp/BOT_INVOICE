import traceback
from db.db_insert_into_logs import db_insert_into_logs


module_name = __name__.split(".")[-1]
description = status = ""

def module_template():
    global description, status, module_name
    try:
        db_insert_into_logs("Log","Do somenthing", module_name)
    except Exception as error:
        db_insert_into_logs("Error",f"An error occurred: Error: [{error}] | Traceback:"
                                    f" [{traceback.format_exc()}] ", module_name)
