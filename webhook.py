"""Methods for calling the webhook"""

import json
import requests


def call_webhook(url, payload):
    """Call the webhook with the given payload."""
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps
    (payload), timeout=10)
    response.raise_for_status()
    return response.status_code