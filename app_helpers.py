import json

from pdf2image import convert_from_bytes
import base64
from io import BytesIO
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def pdf_to_img(pdf: str) -> [str]:
    """
    Takes a base64 encoded string representing a PDF and turns it into a list of base64 encoded strings
    representing pages in the PDF
    :param pdf:
    :return: list of strings
    """
    imgs = list()
    decoded = b64string_to_bytes(pdf)
    images = convert_from_bytes(decoded)
    for img in images:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        buffered.seek(0)
        data_uri = base64.b64encode(buffered.read()).decode('ascii')
        imgs.append(data_uri)
        buffered.close()
        img.close()
    return imgs

def html_to_pdf(string: str, stylesheets: [str]):
    """
    Takes HTML as a string and Stylesheets as list of strings. Wraps a Weasyprint HTML.write_pdf() method
    and returns a base64 encoded bytes object representing the PDF
    :param string:
    :param stylesheets:
    :return:
    """
    font_config = FontConfiguration()
    html= HTML(string=string)
    css_strings = [CSS(string=s, font_config=font_config) for s in stylesheets]
    pdf_bytes = html.write_pdf(target=None, stylesheets=css_strings, font_config=font_config)
    return bytes_to_b64string(pdf_bytes)

 # Helpers
def bytes_to_b64string(bytes: bytes) -> str:
    """
    Simple helper - give me bytes, I'll give you a Base64 encoded string
    :param bytes:
    :return:
    """
    return base64.b64encode(bytes).decode()


def b64string_to_bytes(string: str) -> bytes:
    """
    Inverse of the above
    :param string:
    :return:
    """
    return base64.b64decode(string.encode())

def get_b64_string_from_pdf(pdffile):
    """
    A file reader that provides b64 string output
    :param pdffile:
    :return:
    """

    with open(pdffile, 'rb') as f:
        data = f.read()
        return bytes_to_b64string(data)

def write_file_from_b64string(filename: str, b64string: str) -> int:
    """
    Inverse of the above; decode and write string to filename
    :param filename: filename - ensure write permissions
    :param b64string:
    :return: None
    """

    with open(filename, 'wb') as f:
        bytes = b64string_to_bytes(b64string)
        return f.write(bytes)

def dict_to_b64(payload: dict) -> str:
    """
    Takes a python dict and turns it into a base64 string
    :param payload:
    :return:
    """

    bstring = json.dumps(payload).encode()
    return bytes_to_b64string(bstring)

def b64_to_dict(string: str) -> dict:
    """
    Takes a string and returns a dictionary
    :param string:
    :return:
    """

    binary = b64string_to_bytes(string)
    return json.loads(binary)
