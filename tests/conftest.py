from collections import namedtuple
import pytest
import requests_mock
import tempfile


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
                       'ru-hexlet-io-courses.html',
                       )
_TEST_DATA = namedtuple('TEST_DATA', ['test_url', 'test_404_url', 'test_data_before', 'test_data_after',
                                      'test_img_png', 'test_img_jpg', 'test_app_css',
                                      'test_menu_css', 'test_hw_js', 'test_rel_path_js'])
TEST_DATA = _TEST_DATA('https://ru.hexlet.io/courses',
                       'https://whatever.com/',
                       read_file('tests/fixtures/test_html_before.html'),
                       read_file('tests/fixtures/test_html_after.html'),
                       read_file("tests/fixtures/python.png", mode='rb'),
                       read_file("tests/fixtures/python.jpg", mode='rb'),
                       read_file("tests/fixtures/assets/application.css"),
                       read_file("tests/fixtures/assets/menu.css"),
                       read_file("tests/fixtures/hello_world.js"),
                       read_file("tests/fixtures/relpathscript.js"))


@pytest.fixture(scope='session')
def mock_site():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', TEST_DATA.test_url,
                       text=TEST_DATA.test_data_before, reason='OK', status_code=200)
        m.register_uri('GET', 'https://ru.hexlet.io/assets/python.png',
                       text=str(TEST_DATA.test_img_png), reason='OK', status_code=200)
        m.register_uri('GET', 'https://ru.hexlet.io/assets/python.jpg',
                       text=str(TEST_DATA.test_img_jpg), reason='OK', status_code=200)
        m.register_uri('GET', 'https://ru.hexlet.io/assets/menu.css',
                       text=TEST_DATA.test_menu_css, reason='OK', status_code=200)
        m.register_uri('GET', 'https://ru.hexlet.io/assets/application.css',
                       text=TEST_DATA.test_app_css, reason='OK', status_code=200)
        m.register_uri('GET', 'https://ru.hexlet.io/relpathscript.js',
                       text=TEST_DATA.test_rel_path_js, reason='OK', status_code=200)
        m.register_uri('GET', 'https://ru.hexlet.io/hello_world.js',
                       text=TEST_DATA.test_hw_js, reason='OK', status_code=200)
        m.register_uri('GET', 'https://ru.hexlet.io/courses.html',
                       text=TEST_DATA.test_data_before, reason='OK', status_code=200)
        m.register_uri('GET', 'https://ru.hexlet.io/test.html',
                       text=TEST_DATA.test_data_before, reason='OK', status_code=200)
        m.register_uri('GET', TEST_DATA.test_404_url,
                       text="Oops", reason='Client Error', status_code=404)
        yield


@pytest.fixture()
def tmpdirname(mock_site):
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname
