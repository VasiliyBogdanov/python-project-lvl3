import os
from page_loader.page_loader import download
import pathlib
import pytest
from requests import HTTPError
from tests.conftest import TEST_DATA


def test_directory_doesnt_exist(tmpdirname):
    nonexistent_directory = os.path.join(tmpdirname, 'something')

    with pytest.raises(OSError):
        download(TEST_DATA.test_url, nonexistent_directory)


def test_wrong_file_rights(tmpdirname):
    directory = pathlib.Path(tmpdirname)
    directory.chmod(444)
    permission_denied_path = os.path.join(directory, 'test')

    with pytest.raises(PermissionError):
        download(TEST_DATA.test_url, permission_denied_path)


def test_HTTPError(tmpdirname):
    with pytest.raises(HTTPError):
        download(TEST_DATA.test_404_url, tmpdirname)
