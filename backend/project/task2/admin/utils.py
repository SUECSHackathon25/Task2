from venv import logger
import pandas as pd
import openpyxl
from werkzeug.datastructures.file_storage import FileStorage


def process_judges_file(file: FileStorage):
    logger.debug('hello')
    df = pd.read_excel(file, engine='openpyxl')
    logger.info ('hello')
    logger.debug(df)
    return