import os
import logging
import tempfile


temp_directory = tempfile.mkdtemp(prefix='ExportContacts_', suffix='_temp_folder')
path = os.path.join(temp_directory, 'history.log')
logging.basicConfig(
    filename=path,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger('main_logger')
LOGGER.info(f'Log file location: {path}')
print(f'Log file location: {path}')
