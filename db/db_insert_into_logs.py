import mariadb
import os
import traceback
import keyring
from datetime import datetime
from helper.read_config import (DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_SERVICE,
                                DATABASE_USER_NAME_SERVICE,
                                DEPARTMENT, COUNTRY, PROCESS_NAME, DATABASE_TABLE)


def db_insert_into_logs(status: str, description: str, module_name: str) -> None:

    """

    :rtype: None
    """
    try:
        description = description.strip()
        description = description.replace("\n", "")
        description = description.replace("         ~~^~~", "")
        description = description.replace("^", "")
        description = description.replace("~", "")
        description = description.replace("   ", "")
        description = description.replace("`", "")
        description = description.replace("'", "")
        description = description.replace(";", "")
        description = description.replace('"', "")

        created_at = str(datetime.now())
        user_name = str(os.getlogin())

        # Data assignment
        data = created_at, COUNTRY, DEPARTMENT, PROCESS_NAME, module_name, user_name, status, description

        # Ensuring that connection entries are strings
        db_host = str(DATABASE_HOST).strip()
        db_user = str(DATABASE_USER).strip()
        db_database = str(DATABASE_NAME).strip()

        # Establish a connection to the MySQL server
        db_password = keyring.get_password(DATABASE_SERVICE, DATABASE_USER_NAME_SERVICE)
        conn = mariadb.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database
        )

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # Construct the SQL query for creating the insert statement
        insert_query = f"INSERT INTO {DATABASE_TABLE} VALUES ({', '.join(['%s'] * len(data))})"

        # Execute the query to insert data
        cursor.execute(insert_query, data)

        # Commit changes and close the connection
        conn.commit()
        conn.close()
    except mariadb.Error as error:
        print(f"Error inserting data: {error}")
        print(f'[{traceback.format_exc()}].\n**************************************************************************')