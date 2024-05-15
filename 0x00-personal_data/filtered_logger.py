#!/usr/bin/env python3
""" Filtered Logger """
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """ Returns the log message obfuscated.

    Args:
        fields (List[str]): list of fields to obfuscate
        redaction (str): the obfuscation string
        message (str): the log message
        separator (str): the separator for the message
    """
    for field in fields:
        pattern = field + "=.*?" + separator
        message = re.sub(pattern, field + "=" + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the record
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Returns a logging object
    """
    user_data = logging.getLogger('user_data')
    user_data.setLevel(logging.INFO)
    user_data.propagate = False
    user_data.handlers.clear()
    user_data.addHandler(logging.StreamHandler())
    user_data.handlers[0].setFormatter(RedactingFormatter(list(PII_FIELDS)))
    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to a MySQL database
    """
    try:
        db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
        db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
        db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
        db_name = os.getenv('PERSONAL_DATA_DB_NAME', 'holberton')

        connection = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
        )

        return connection
    except mysql.connector.Error as err:
        return None


def main():
    """ Main function
    """
    formatter = RedactingFormatter(list(PII_FIELDS))
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        record = logging.LogRecord("user_data", logging.INFO, None,
                                   None, str(row), None, None)
        print(formatter.format(record))

    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
