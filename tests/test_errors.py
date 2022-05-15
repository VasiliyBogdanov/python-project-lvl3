import os
from page_loader.page_loader import download
import pathlib
import pytest
from requests import HTTPError
import requests_mock
import tempfile
from tests.test_page_loader import test_url
from tests.test_page_loader import test_data_before


def test_directory_doesnt_exist():
    with tempfile.TemporaryDirectory() as tmpdirname:
        nonexistent_directory = os.path.join(tmpdirname, 'something')
        with pytest.raises(OSError):
            download(test_url, nonexistent_directory)


def test_wrong_file_rights():
    with tempfile.TemporaryDirectory() as tmpdirname:
        directory = pathlib.Path(tmpdirname)
        directory.chmod(444)
        permission_denied_path = os.path.join(directory, 'test')

        with pytest.raises(PermissionError):
            download(test_url, permission_denied_path)


def test_HTTPError():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', test_url, text=test_data_before, reason='Client Error', status_code=404)

        with tempfile.TemporaryDirectory() as tmpdirname:
            with pytest.raises(HTTPError):
                download(test_url, tmpdirname)
