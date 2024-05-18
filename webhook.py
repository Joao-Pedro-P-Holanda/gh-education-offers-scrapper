"""Methods for calling the webhook"""

import json
import logging
import requests


def call_webhook(url, payload):
    """Call the webhook with the given payload."""
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps
    (payload), timeout=10)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(f"""Error calling webhook on url {url} code-{err.response.status_code} reason-{err.response.reason}""")
    return response.status_code