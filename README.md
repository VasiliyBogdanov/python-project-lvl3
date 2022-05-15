### Hexlet tests and linter status:
[![Actions Status](https://github.com/VasiliyBogdanov/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/VasiliyBogdanov/python-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/835c25dc194cb9cb75b1/maintainability)](https://codeclimate.com/github/VasiliyBogdanov/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/835c25dc194cb9cb75b1/test_coverage)](https://codeclimate.com/github/VasiliyBogdanov/python-project-lvl3/test_coverage)
[![flake8](https://github.com/VasiliyBogdanov/python-project-lvl3/actions/workflows/flake8.yml/badge.svg)](https://github.com/VasiliyBogdanov/python-project-lvl3/actions/workflows/flake8.yml)  
This is the third project in Hexlet's 'Python developer' course, 'page-loader'.  
Downloads web page with it's resources.  

### Specs:
- can be used as a library or through CLI
- works with __static__ web pages, only downloads __local__ resources from 'img', 'link' and 'script' tags
- allowed img formats are .png and .jpg
- downloads web pages inside 'link' tags (without downloading their resources)
- downloads resource from 'script' tag only if it has src attribute. Also ignores inline code inside 'script' tags  

### Requirements:
- Python 3.8 or higher
- poetry
### Example of page-loader CLI
[![asciicast](https://asciinema.org/a/SBLIOFXpSGb2C901apI6Q0II8.svg)](https://asciinema.org/a/SBLIOFXpSGb2C901apI6Q0II8)