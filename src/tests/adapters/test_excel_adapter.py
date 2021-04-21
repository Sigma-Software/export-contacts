import os
from stat import S_IRUSR
from tempfile import mkdtemp

import pytest

from adapters.excel_adapter import create_xlsx_file
from domain.entities import ExportContactException


class TestExcelAdapter:
    username = 'test_user_name'

    def test_create_xlsx_file(self):
        temp_directory = mkdtemp(prefix='ExportContactsTests_')
        path = os.path.abspath(temp_directory)
        test = create_xlsx_file(self.username, dict(), path)
        assert test is None
        assert os.path.exists(temp_directory)
        assert len(os.listdir(path)) == 1
        assert os.listdir(path)[0].startswith(self.username) and os.listdir(path)[0].endswith('.xlsx')
        os.chmod(path, S_IRUSR)

        with pytest.raises(ExportContactException):
            create_xlsx_file(self.username, dict(), path)
