import json
from unittest import TestCase, skip
from app_helpers import html_to_pdf, pdf_to_img, b64string_to_bytes, bytes_to_b64string, get_b64_string_from_pdf, \
    write_file_from_b64string, dict_to_b64, b64_to_dict
from app import handler
import base64
import requests


class Html2PdfTestcase(TestCase):

    def test_encoder_decoder_function(self):
        bytes = b"This is my fancy bytestring"
        con_recon = b64string_to_bytes(bytes_to_b64string(bytes))
        self.assertEqual(bytes, con_recon)

    def test_get_b64string_from_pdf(self):
        bstring = get_b64_string_from_pdf("./40000_report.pdf")
        self.assertEqual("JVBER", bstring[:5])

    def test_dict_to_b64(self):
        obj = {
            'function': 'something',
            'kwargs': {}
        }

        res = dict_to_b64(obj)
        self.assertEqual(res, "eyJmdW5jdGlvbiI6ICJzb21ldGhpbmciLCAia3dhcmdzIjoge319")

    def test_b64_to_dict(self):
        res = b64_to_dict("eyJmdW5jdGlvbiI6ICJzb21ldGhpbmciLCAia3dhcmdzIjoge319")
        self.assertEqual(res['function'], 'something')

    def test_read_write_file(self):
        bstring = get_b64_string_from_pdf("./40000_report.pdf")
        out = write_file_from_b64string(filename="./40000_copy.pdf", b64string=bstring)
        self.assertEqual(out, 52096)
        bstring2 = get_b64_string_from_pdf("./40000_copy.pdf")
        self.assertEqual("JVBER", bstring2[:5])

    def test_html_to_pdf(self):
        html_string = '<h1>The title</h1>'
        css_string = '''
    @font-face {
        font-family: Gentium;
        src: url(http://example.com/fonts/Gentium.otf);
    }
    h1 { font-family: Gentium }
    '''
        res = html_to_pdf(html_string, [css_string])
        pdf = base64.b64decode(res.encode())
        self.assertEqual(pdf[:4], b'%PDF')

    def test_pdf_to_img(self):
        html_string = '<h1>The title</h1>'
        css_string = '''
            @font-face {
                font-family: Gentium;
                src: url(http://example.com/fonts/Gentium.otf);
            }
            h1 { font-family: Gentium }
            '''
        res = html_to_pdf(html_string, [css_string])
        pdf = base64.b64decode(res.encode())
        self.assertEqual(pdf[:4], b'%PDF')

        res = pdf_to_img(res)
        self.assertEqual(len(res), 1)
        img = base64.b64decode(res[0].encode())
        self.assertEqual(b'\x89PNG', img[:4])


class HandlerTestCase(TestCase):

    def test_handler_html_to_pdf(self):
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
                'stylesheets': [css_string]
            }
        }

        event = {
            'body': dict_to_b64(body)
        }

        res = handler(event=event, context=None)
        self.assertEqual(res['statusCode'], 200)
        result = json.loads(res['body'])['result']
        pdf = base64.b64decode(result.encode())
        self.assertEqual(pdf[:4], b'%PDF')

    def test_handler_pdf_to_img(self):
        html_string = '<h1>The title</h1>'
        css_string = '''
            @font-face {
                font-family: Gentium;
                src: url(http://example.com/fonts/Gentium.otf);
            }
            h1 { font-family: Gentium }
            '''
        res = html_to_pdf(html_string, [css_string])
        pdf = base64.b64decode(res.encode())
        self.assertEqual(pdf[:4], b'%PDF')

        body = {
            'function': 'pdf_to_img',
            'kwargs': {
                'pdf': res
            }
        }

        event = {
            'body': dict_to_b64(body)
        }

        res = handler(event=event, context=None)
        self.assertEqual(res['statusCode'], 200)
        result = json.loads(res['body'])['result']
        self.assertEqual(len(result), 1)
        img = base64.b64decode(result[0].encode())
        self.assertEqual(b'\x89PNG', img[:4])

    def test_handler_in_docker(self):
        """
        Make sure Docker is running on port 9000
        :return:
        """

        html_string = '<h1>The title</h1>'
        css_string = '''
                    @font-face {
                        font-family: Gentium;
                        src: url(http://example.com/fonts/Gentium.otf);
                    }
                    h1 { font-family: Gentium }
                    '''
        res = html_to_pdf(html_string, [css_string])
        pdf = base64.b64decode(res.encode())
        self.assertEqual(pdf[:4], b'%PDF')

        body = {
            'function': 'pdf_to_img',
            'kwargs': {
                'pdf': res
            }
        }

        event = {
            'body': json.dumps(body)
        }

        res = requests.post("http://localhost:9000/2015-03-31/functions/function/invocations",
                            json=event)
        self.assertEqual(res.status_code, 200)


class LiveHandlerTestCase(TestCase):

    def test_handler_live(self):
        html_string = '<h1>The title</h1>'
        css_string = '''
                            @font-face {
                                font-family: Gentium;
                                src: url(http://example.com/fonts/Gentium.otf);
                            }
                            h1 { font-family: Gentium }
                            '''
        res = html_to_pdf(html_string, [css_string])
        pdf = base64.b64decode(res.encode())
        self.assertEqual(pdf[:4], b'%PDF')

        body = {
            'function': 'pdf_to_img',
            'kwargs': {
                'pdf': res
            }
        }

        import os
        url = os.environ.get('LIVE_URL')

        res = requests.post(url=url, json=body)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.content)['result'][0][:5], "iVBOR")
