from collections import namedtuple

_tag_names = namedtuple('TAG', 'img link script')
TAG_NAMES = _tag_names('img', 'link', 'script')

_TAGS = namedtuple('TAGS', 'img link script')
TAG_LINKS = _TAGS('src', 'href', 'src')

FILES_FOLDER_SUFFIX = '_files'
HTML_SUFFIX = '.html'

_resource_tags = namedtuple('Resources', 'img link script')
