from page_loader.page_loader import download, format_filename
from collections import namedtuple
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
    _RESOURCES = namedtuple('RESOURCES', 'img_png img_jpg app_css menu_css hw_js rel_path_script_js courses_html')
    RESOURCES = _RESOURCES('assets-python.png',
                           'assets-python.jpg',
                           'assets-application.css',
                           'assets-menu.css',
                           'hello-world.js',
                           'rel-path-script.js',
                           'courses.html'
                           )

    test_url = 'https://ru.hexlet.io/courses'
    test_data_before = read_file('tests/fixtures/test_html_before.html')
    test_data_after = read_file('tests/fixtures/test_html_after.html')
    test_img_png = read_file("tests/fixtures/python.png", mode='rb')
    test_img_jpg = read_file("tests/fixtures/python.png", mode='rb')
    test_app_css = read_file("tests/fixtures/assets/application.css")
    test_menu_css = read_file("tests/fixtures/assets/menu.css")
    test_hw_js = read_file("tests/fixtures/hello_world.js")
    test_rel_path_js = read_file("tests/fixtures/rel_path_script.js")
    test_courses_html = test_data_before

    with requests_mock.Mocker() as m:
        m.get(test_url, text=test_data_before)
        m.get('https://ru.hexlet.io/courses/assets/python.png', text=str(test_img_png))
        m.get('https://ru.hexlet.io/courses/assets/python.jpg', text=str(test_img_jpg))
        m.get('https://ru.hexlet.io/assets/menu.css', text=test_menu_css)
        m.get('https://ru.hexlet.io/assets/application.css', text=test_app_css)
        m.get('https://ru.hexlet.io/rel_path_script.js', text=test_rel_path_js)
        m.get('https://ru.hexlet.io/hello_world.js', text=test_hw_js)

        with tempfile.TemporaryDirectory() as tmpdirname:
            result = download(test_url, tmpdirname)

            # Test correctness of .html creation path
            assert result == os.path.join(tmpdirname, format_filename(test_url, '.html'))

            # Test correctness of created .html structure
            result_html_data = read_file(result)
            assert test_data_after == result_html_data

            # Test that .html file and '_files' folder were created
            assert format_filename(test_url, '.html') in os.listdir(tmpdirname)
            assert format_filename(test_url, '_files') in os.listdir(tmpdirname)

            # Test that files was downloaded
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
