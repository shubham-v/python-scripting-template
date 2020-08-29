def query_params_string(params):
    query_string = ''
    for k,v in params.items():
        query_string += k + '=' + v + '&'
    return query_string[:-1]