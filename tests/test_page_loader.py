from page_loader.page_loader import download, format_filename
import os
import requests_mock
import tempfile


# Test format_name
def test_format_name():
    url_without_extension = 'https://ru.hexlet.io/courses'
    url_with_extension = 'https://ru.hexlet.io/courses/about.html'

    assert format_filename(url_without_extension) == 'ru-hexlet-io-courses.html'
    assert format_filename(url_with_extension) == 'ru-hexlet-io-courses-about.html'


# Test download
def test_download():
    test_data = 'data'
    test_url = 'https://ru.hexlet.io/courses'
    with requests_mock.Mocker() as m:
        m.get(test_url, text=test_data)
        with tempfile.TemporaryDirectory() as tmpdirname:
            result = download(test_url, tmpdirname)
            assert result == os.path.join(tmpdirname, format_filename(test_url))
            with open(result, mode='r') as f:
                data = f.read()
                assert data == test_data
