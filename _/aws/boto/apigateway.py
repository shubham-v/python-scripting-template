import boto3
import requtils
import logging


def invoke(api_id, resource_id, method, path, request_params={}, headers={}, body=''):
    path, query_params_string = get_path_query_params(path, request_params)

    client = boto3.client('apigateway')
    log_msg = 'Invoking ApiGateway:: ApiId: {api}, ResourceId: {resource}, Method: {method}, Path: {path}'\
        .format(api=api_id, resource=resource_id, method=method, body=body, headers=headers, path=path)
    logging.info(log_msg)
    logging.info('Request Body: {body}'.format(body=body))
    logging.info('Headers: {headers}'.format(headers=headers))
    response = None
    try:
        response = client.test_invoke_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            body=body,
            headers=headers,
            pathWithQueryString=path,
        )
        response = handle_response(response, log_msg)
    except Exception as e:
        logging.error('Error occured while {msg}'.format(msg=log_msg), exc_info=True)
    return response

def handle_response(response, log_msg):
    logResponse(response)
    if response['status'] != 200:
        logging.error('Invalid response received for {msg}'.format(msg=log_msg))
        return None
    return response['body']

def logResponse(response):
    logging.info('Response:: Status: {code}, Body: {payload}'.format(code=response['status'], payload=response['body']))

def get_path_query_params(path, request_params):
    query_params_string = requtils.query_params_string(request_params)
    if query_params_string != '':
        path = '{path}?{queryparams}'.format(path=path, queryparams=query_params_string)
    return path, query_params_string