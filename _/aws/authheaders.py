import hmac
import hashlib
import os
import sys
import datetime
import config
import requtils

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(("AWS4" + key).encode("utf-8"), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, "aws4_request")
    return kSigning

def keys(access_key, secret_key):
    if access_key is None: access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    if secret_key is None: secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    if access_key is None or secret_key is None:
        print('No access key is available.')
        sys.exit()
    return access_key, secret_key

def headers(host, request_params, payload, method):
    return headers(host=host, request_parameters=request_params, payload='', method=method,
                   region=config.cfg['region'], service=config.cfg['service'],
                   access_key=config.cfg['AWS_ACCESS_KEY_ID'], secret_key=config.cfg['AWS_SECRET_ACCESS_KEY'])

def headers(host, request_parameters, payload, method, region, service, access_key, secret_key):
    """
    :param host: endpoint
    :param request_parameters: query_params
    :param payload: The request body
    :param method: The Request method
    :param region: The AWS region
    :param service: The aws service
    :param access_key: AWS_ACCESS_KEY_ID
    :param secret_key: AWS_SECRET_ACCESS_KEY
    :return: header 'x-amz-date', 'Authorization'
    https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
    """
    request_parameters = requtils.query_params_string(request_parameters)
    access_key, secret_key = keys(access_key, secret_key)
    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')
    canonical_uri = '/'
    canonical_querystring = request_parameters
    canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
    signed_headers = 'host;x-amz-date'
    payload_hash = hashlib.sha256((payload).encode('utf-8')).hexdigest()
    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' + amzdate + '\n' + credential_scope + '\n' + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    signing_key = getSignatureKey(secret_key, datestamp, region, service)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
    headers = {'x-amz-date': amzdate, 'Authorization': authorization_header}
    return headers
