from page_loader.page_loader import download, format_filename
import os
import requests_mock
import tempfile


def read_file(path, mode='r'):
    with open(path, mode=mode) as f:
        return str(f.read()).strip()


# Test format_name
def test_format_filename():
    url_without_extension = 'https://ru.hexlet.io/courses'
    url_with_extension = 'https://ru.hexlet.io/courses/about.html'

    assert format_filename(url_without_extension, '.html') == 'ru-hexlet-io-courses.html'
    assert format_filename(url_with_extension, '.html') == 'ru-hexlet-io-courses-about.html'


# Test download
def test_download():
    test_data_before = read_file('tests/fixtures/test_html_before.html')
    test_data_after = read_file('tests/fixtures/test_html_after.html')
    test_img_png = read_file('tests/fixtures/python.png', mode='rb')
    test_img_jpg = read_file('tests/fixtures/python.jpg', mode='rb')
    test_url = 'https://ru.hexlet.io/courses'

    with requests_mock.Mocker() as m:
        m.get(test_url, text=test_data_before)
        m.get('https://ru.hexlet.io/courses/assets/python.png', text=test_img_png)
        m.get('https://ru.hexlet.io/courses/assets/python.jpg', text=test_img_jpg)
        with tempfile.TemporaryDirectory() as tmpdirname:
            result = download(test_url, tmpdirname)

            # Test correctness of .html creation path
            assert result == os.path.join(tmpdirname, format_filename(test_url, '.html'))

            # Test correctness of created .html structure
            result_html_data = read_file(result)
            assert test_data_after == result_html_data

            # Test that .html file and 'files' folder were created
            assert format_filename(test_url, '.html') in os.listdir(tmpdirname)
            assert format_filename(test_url, '_files') in os.listdir(tmpdirname)

            # Test, that img was downloaded
            downloaded_image_path = os.path.join(tmpdirname, os.listdir(tmpdirname)[0])
            downloaded_image_dir = os.listdir(downloaded_image_path)
            assert 'assets-python.png' in downloaded_image_dir
            assert 'assets-python.jpg' in downloaded_image_dir

            # Test correctness of downloaded img
            downloaded_png = read_file(os.path.join(downloaded_image_path, downloaded_image_dir[0]))
            downloaded_jpg = read_file(os.path.join(downloaded_image_path, downloaded_image_dir[1]))
            assert downloaded_png == test_img_png
            assert downloaded_jpg == test_img_jpg
