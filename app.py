import json
import app_helpers


def handler(event, context):
    """
    Dispatcher based on converstion request in event
    :param event: a serialized JSON object containing a 'body' object
    event = {
        'body': {
            'function': function_name, either 'pdf_to_img' or 'html_to_pdf',
            'kwargs': {
                'key': 'value' - see documentation for functions below
            }
        }
    }
    :param context:
    :return:
    """
    try:
        body = event.get('body')
        payload = app_helpers.b64_to_dict(body)
        function = getattr(app_helpers, payload['function'])
        kwargs = payload['kwargs']
        result = function(**kwargs)

        output = {
            'result': result,
            'function': payload['function']
        }

        return {
            'statusCode': 200,
            'body': json.dumps(output),
            "isBase64Encoded": False,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }

    except Exception as e:
        return {
            'statusCode': 406,
            'body': repr(e),
            "isBase64Encoded": False,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
