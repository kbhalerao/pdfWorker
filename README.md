# PDFWorker

A containerized lambda service for HTML to PDF generation

See the `tests_unit_functions.py` for usage and examples. 

## Basic usage 
### for `html_to_pdf`:

```python
import requests

html_string = '<h1>The title</h1>'
css_string = '''
    @font-face {
        font-family: Gentium;
        src: url(http://example.com/fonts/Gentium.otf);
    }
    h1 { font-family: Gentium }
'''

body = {
    'function': 'html_to_pdf',
    'kwargs': {
        'string': html_string, 
        'css': [css_string]
    }
}

res = requests.post(url=<LIVE URL>, json=body)
```

### for `pdf_to_img`

```python
from app_helpers import get_b64_string_from_pdf
import requests

body = {
    'function': 'pdf_to_img',
    'kwargs': {
        'pdf': get_b64_string_from_pdf(pdffile)
    }
}

res = requests.post(url=url, json=body)
```