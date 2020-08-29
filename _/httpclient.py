import requests
import json
import logging

HEADERS = {
    'Content-type': 'application/json'
}

def get(url, params, headers={}, timeout_milliseconds=None):
    """Constructs a GET request, prepares it and sends it.
               Returns : response.
       :param url: The URL for posting request
       :param params: The payloadparams to be sent in the request
       :param headers: The headers
       :param timeout_milliseconds: The connection/socket timeout in milliseconds
       """
    log_msg = 'Invoking Url: {url} with query params {params}'.format(url=url, params=params)
    logging.info(log_msg)
    logging.info('Headers: {headers}'.format(headers=headers))
    response = None
    try:
        response = requests.get(url=url, params=params, headers=headers, timeout=timeout_milliseconds)
        response = handleResponse(response, log_msg)
    except (requests.ConnectTimeout, requests.ConnectionError) as e:
        logConnectionTimeOut(log_msg)
    except Exception as e:
        logging.error('Error occured while {msg}'.format(msg=log_msg), exc_info=True)
    return response

def post(url, headers={}, payload='', timeout_milliseconds=None):
    """Constructs a POST request, prepares it and sends it.
            Returns : response.
    :param url: The URL for posting request
    :param payload: The payload to be sent in the request
    :param timeoutMilliseconds: The connection/socket timeout in milliseconds
    """
    headers = dict(headers.items() + HEADERS.items())
    log_msg = 'Invoking URL: {msg}'.format(msg=url)
    logging.info(log_msg)
    logging.info('Request Payload: {msg}'.format(msg=payload))
    logging.info('Headers: {headers}'.format(headers=headers))
    response = None
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(payload), timeout=timeout_milliseconds)
        response = handleResponse(response)
    except (requests.ConnectTimeout, requests.ConnectionError) as e:
        logConnectionTimeOut(log_msg, e)
    except Exception as e:
        logging.error('Error occured while {msg}'.format(msg=log_msg), exc_info=True)
    return response

def handleResponse(response, log_msg):
    logResponse(response)
    if response.status_code != 200:
        logging.error('Invalid response received for {msg}'.format(msg=log_msg))
        return None
    return response._content

def logConnectionTimeOut(log_msg, e):
    logging.exception('Connection Timed out while {msg}'.format(msg=log_msg))

def logResponse(response):
    logging.info('Response:: Status: {code}, Body: {payload}'.format(code=response.status_code, payload=response._content))