from collections import namedtuple

_TAGS = namedtuple('TAGS', 'img link script')
TAG_LINKS = _TAGS('src', 'href', 'src')

FILES_FOLDER_SUFFIX = '_files'
HTML_SUFFIX = '.html'
