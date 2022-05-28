import os
from page_loader.formatters import format_host_name
from page_loader.page_loader import download
from page_loader.paths import FILES_FOLDER_SUFFIX
from page_loader.errors import HTML_SUFFIX
from pathlib import Path
from tests.conftest import read_file
from tests.conftest import RESOURCES
from tests.conftest import TEST_DATA


def test_download_path_creation(tmpdirname):
    result = download(TEST_DATA.test_url, tmpdirname)

    assert Path(result) == Path(os.path.join(tmpdirname, format_host_name(TEST_DATA.test_url) + '.html'))


def test_downloaded_html_structure(tmpdirname):
    result = download(TEST_DATA.test_url, tmpdirname)
    result_html_data = read_file(result)

    assert TEST_DATA.test_data_after == result_html_data


def test_main_html_file_creation(tmpdirname):
    download(TEST_DATA.test_url, tmpdirname)
    assert format_host_name(TEST_DATA.test_url) + HTML_SUFFIX in os.listdir(tmpdirname)


def test_files_folder_creation(tmpdirname):
    download(TEST_DATA.test_url, tmpdirname)
    assert format_host_name(TEST_DATA.test_url) + FILES_FOLDER_SUFFIX in os.listdir(tmpdirname)


def test_downloaded_files(tmpdirname):
    download(TEST_DATA.test_url, tmpdirname)
    files_directory = list(i for i in os.listdir(tmpdirname) if i.endswith(FILES_FOLDER_SUFFIX))[0]
    downloaded_files_path = os.path.join(tmpdirname, files_directory)
    downloaded_files_dir = os.listdir(downloaded_files_path)

    downloaded_png = read_file(os.path.join(downloaded_files_path, RESOURCES.img_png))
    downloaded_jpg = read_file(os.path.join(downloaded_files_path, RESOURCES.img_jpg))
    downloaded_app_css = read_file(os.path.join(downloaded_files_path, RESOURCES.app_css))
    downloaded_menu_css = read_file(os.path.join(downloaded_files_path, RESOURCES.menu_css))
    downloaded_hw_js = read_file(os.path.join(downloaded_files_path, RESOURCES.hw_js))
    downloaded_rel_path_script_js = read_file(os.path.join(downloaded_files_path, RESOURCES.rel_path_script_js))
    downloaded_courses_html = read_file(os.path.join(downloaded_files_path, RESOURCES.courses_html))

    assert RESOURCES.img_png in downloaded_files_dir
    assert RESOURCES.img_jpg in downloaded_files_dir
    assert RESOURCES.app_css in downloaded_files_dir
    assert RESOURCES.menu_css in downloaded_files_dir
    assert RESOURCES.hw_js in downloaded_files_dir
    assert RESOURCES.rel_path_script_js in downloaded_files_dir
    assert RESOURCES.courses_html in downloaded_files_dir

    assert downloaded_png == str(TEST_DATA.test_img_png)
    assert downloaded_jpg == str(TEST_DATA.test_img_jpg)
    assert downloaded_app_css == TEST_DATA.test_app_css
    assert downloaded_menu_css == TEST_DATA.test_menu_css
    assert downloaded_hw_js == TEST_DATA.test_hw_js
    assert downloaded_rel_path_script_js == TEST_DATA.test_rel_path_js
    assert downloaded_courses_html == TEST_DATA.test_data_before


def test_logging(caplog, tmpdirname):
    download(TEST_DATA.test_url, tmpdirname)
    with open('tests/fixtures/test_log_messages.log', mode='r') as f:
        data = [i.strip() for i in f.readlines()]
    assert caplog.messages == data


def test_empty_html(tmpdirname):
    download(TEST_DATA.test_empty, tmpdirname)
    directory = os.listdir(tmpdirname)
    assert 'empty-com.html' in directory
    assert 'empty-com_files' not in directory
