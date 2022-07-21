### Hexlet tests and linter status:
[![Actions Status](https://github.com/VasiliyBogdanov/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/VasiliyBogdanov/python-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/835c25dc194cb9cb75b1/maintainability)](https://codeclimate.com/github/VasiliyBogdanov/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/835c25dc194cb9cb75b1/test_coverage)](https://codeclimate.com/github/VasiliyBogdanov/python-project-lvl3/test_coverage)
[![flake8](https://github.com/VasiliyBogdanov/python-project-lvl3/actions/workflows/flake8.yml/badge.svg)](https://github.com/VasiliyBogdanov/python-project-lvl3/actions/workflows/flake8.yml) 
### Description:
This is the 3rd project in Hexlet's 'Python developer' course, 'page-loader'.  
Downloads web page with it's resources.  

### Specs:
- can be used as a library or through CLI
- works with __static__ web pages, only downloads __local__ resources from 'img', 'link' and 'script' tags
- downloads web pages inside 'link' tags (without downloading their resources)
- ignores inline code inside 'script' tags  

### Requirements:
- Python 3.8 or higher
- poetry
### Installation:
```
pip install git+https://github.com/VasiliyBogdanov/python-project-lvl3.git
```
or:
- Clone this repo;
- If you have 'make' utility:
```
make install
make build
make publish
make package-install
```
- If you don't:
    - get one 🧐  
or:
```
poetry install
poetry build
poetry publish --dry-run
python3 -m pip install --user dist/*.whl
```
### Usage:
CLI
```
page-loader url directory
```
Function
```
some_var = download(url, directory)
```
Default for 'directory' is current working directory.
### Example of page-loader CLI
[![asciicast](https://asciinema.org/a/SBLIOFXpSGb2C901apI6Q0II8.svg)](https://asciinema.org/a/SBLIOFXpSGb2C901apI6Q0II8)
