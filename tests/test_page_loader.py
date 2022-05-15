from collections import namedtuple
import os
from page_loader.formatters import format_host_name
from page_loader.logger import get_logger
from page_loader.logger import get_standard_file_handler
from page_loader.logger import get_standard_stream_handler
from page_loader.page_loader import download
from pathlib import Path
import requests_mock
import tempfile


def make_test_logger(log_dir, log_name):
    test_logger = get_logger('test')
    log_filepath = os.path.join(log_dir, log_name)
    test_logger.addHandler(get_standard_file_handler(log_filepath, mode='w'))
    test_logger.addHandler(get_standard_stream_handler())
    return test_logger


def read_file(path, mode='r'):
    with open(path, mode=mode) as f:
        return str(f.read()).strip()


_RESOURCES = namedtuple('RESOURCES', 'img_png img_jpg app_css menu_css hw_js rel_path_script_js courses_html')
RESOURCES = _RESOURCES('ru-hexlet-io-assets-python.png',
                       'ru-hexlet-io-assets-python.jpg',
                       'ru-hexlet-io-assets-application.css',
                       'ru-hexlet-io-assets-menu.css',
                       'ru-hexlet-io-hello-world.js',
                       'ru-hexlet-io-relpathscript.js',
                       'ru-hexlet-io-courses.html'
                       )

test_url = 'https://ru.hexlet.io/courses'
test_data_before = read_file('tests/fixtures/test_html_before.html')
test_data_after = read_file('tests/fixtures/test_html_after.html')
test_img_png = read_file("tests/fixtures/python.png", mode='rb')
test_img_jpg = read_file("tests/fixtures/python.jpg", mode='rb')
test_app_css = read_file("tests/fixtures/assets/application.css")
test_menu_css = read_file("tests/fixtures/assets/menu.css")
test_hw_js = read_file("tests/fixtures/hello_world.js")
test_rel_path_js = read_file("tests/fixtures/relpathscript.js")
test_courses_html = test_data_before
test_test_html = test_data_before


def test_download(caplog):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', test_url, text=test_data_before, reason='OK')
        m.register_uri('GET', 'https://ru.hexlet.io/assets/python.png', text=str(test_img_png), reason='OK')
        m.register_uri('GET', 'https://ru.hexlet.io/assets/python.jpg', text=str(test_img_jpg), reason='OK')
        m.register_uri('GET', 'https://ru.hexlet.io/assets/menu.css', text=test_menu_css, reason='OK')
        m.register_uri('GET', 'https://ru.hexlet.io/assets/application.css', text=test_app_css, reason='OK')
        m.register_uri('GET', 'https://ru.hexlet.io/relpathscript.js', text=test_rel_path_js, reason='OK')
        m.register_uri('GET', 'https://ru.hexlet.io/hello_world.js', text=test_hw_js, reason='OK')
        m.register_uri('GET', 'https://ru.hexlet.io/courses.html', text=test_courses_html, reason='OK')
        m.register_uri('GET', 'https://ru.hexlet.io/test.html', text=test_test_html, reason='OK')

        with tempfile.TemporaryDirectory() as tmpdirname:
            test_logger = make_test_logger(tmpdirname, 'test.log')
            result = download(test_url, tmpdirname, log=True, logger=test_logger)

            # Test correctness of .html creation path
            assert Path(result) == Path(os.path.join(tmpdirname, format_host_name(test_url) + '.html'))

            # Test correctness of created .html structure
            result_html_data = read_file(result)
            assert test_data_after == result_html_data

            # Test that .html file and '_files' folder were created
            assert format_host_name(test_url) + '.html' in os.listdir(tmpdirname)
            assert format_host_name(test_url) + '_files' in os.listdir(tmpdirname)

            # Test that files were downloaded
            files_directory = list(i for i in os.listdir(tmpdirname) if i.endswith('_files'))[0]
            downloaded_files_path = os.path.join(tmpdirname, files_directory)
            downloaded_files_dir = os.listdir(downloaded_files_path)

            assert RESOURCES.img_png in downloaded_files_dir
            assert RESOURCES.img_jpg in downloaded_files_dir

            assert RESOURCES.app_css in downloaded_files_dir
            assert RESOURCES.menu_css in downloaded_files_dir

            assert RESOURCES.hw_js in downloaded_files_dir
            assert RESOURCES.rel_path_script_js in downloaded_files_dir

            assert RESOURCES.courses_html in downloaded_files_dir

            # Test correctness of downloaded files
            downloaded_png = read_file(os.path.join(downloaded_files_path, RESOURCES.img_png))
            downloaded_jpg = read_file(os.path.join(downloaded_files_path, RESOURCES.img_jpg))

            downloaded_app_css = read_file(os.path.join(downloaded_files_path, RESOURCES.app_css))
            downloaded_menu_css = read_file(os.path.join(downloaded_files_path, RESOURCES.menu_css))

            downloaded_hw_js = read_file(os.path.join(downloaded_files_path, RESOURCES.hw_js))
            downloaded_rel_path_script_js = read_file(os.path.join(downloaded_files_path, RESOURCES.rel_path_script_js))

            downloaded_courses_html = read_file(os.path.join(downloaded_files_path, RESOURCES.courses_html))

            assert downloaded_png == str(test_img_png)
            assert downloaded_jpg == str(test_img_jpg)

            assert downloaded_app_css == test_app_css
            assert downloaded_menu_css == test_menu_css

            assert downloaded_hw_js == test_hw_js
            assert downloaded_rel_path_script_js == test_rel_path_js

            assert downloaded_courses_html == test_courses_html

            # Test log messages (without time recorded)
            with open('tests/fixtures/test_log_messages.log', mode='r') as f:
                data = [i.strip() for i in f.readlines()]
            assert caplog.messages == data
