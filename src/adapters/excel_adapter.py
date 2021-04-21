import os
from datetime import datetime
from typing import ValuesView

import xlsxwriter

from domain.entities import ExportContactException, Contact
from utils.logger import LOGGER


EXCEL_FILE_ENDING = '_contacts.xlsx'


def create_xlsx_file(username: str, contacts: ValuesView, path: str) -> None:
    """Creates excel file in chosen directory and writes data with contacts"""
    current_datetime = str(datetime.now().strftime('%d-%m-%Y_%H-%M'))

    LOGGER.info('Creating .xlsx file.')
    LOGGER.info(f'File path: {os.path.abspath(path)}')

    workbook = xlsxwriter.Workbook(os.path.join(
        os.path.abspath(path),
        username.split('\\')[-1] + '_' + current_datetime + EXCEL_FILE_ENDING
    ))

    worksheet = workbook.add_worksheet()
    row = 1
    col = 0
    for title in Contact.__dataclass_fields__:
        worksheet.write(0, col, title)
        col += 1

    for contact in contacts:
        col = 0
        for i in contact.__dict__.values():
            worksheet.write(row, col, str(i))
            col += 1
        row += 1

    try:
        workbook.close()
        LOGGER.info(
            f'File was successfully created with name: '
            f'{username}_{current_datetime}{EXCEL_FILE_ENDING}'
        )
        LOGGER.info('Export ended')
    except xlsxwriter.exceptions.FileCreateError as ex:
        LOGGER.error(
            f'Can not to create file in this directory. '
            f'Full text of error: {str(ex)}'
        )
        raise ExportContactException(
            'It is impossible to create file in the specified folder. '
            'Please choose another one and try again.'
        )
