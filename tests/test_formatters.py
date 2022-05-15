from page_loader.formatters import format_filename
from page_loader.formatters import format_host_name
import pytest


@pytest.mark.parametrize("test_input, expected", [
    (format_filename('https://ru.hexlet.io/assets/python.png'), 'ru-hexlet-io-assets-python.png'),
    (format_filename('ru.hexlet.io/courses') + '.html', 'ru-hexlet-io-courses.html'),
])
def test_format_filename(test_input, expected):
    assert test_input == expected


@pytest.mark.parametrize("test_input, expected", [
    (format_host_name('https://ru.hexlet.io/courses'), 'ru-hexlet-io-courses'),
    (format_host_name('https://ru.hexlet.io/courses/'), 'ru-hexlet-io-courses'),
    (format_host_name('https://ru.hexlet.io'), 'ru-hexlet-io'),
])
def test_format_host_name(test_input, expected):
    assert test_input == expected
