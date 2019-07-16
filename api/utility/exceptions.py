from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    #TODO: If the request fails such as by feature param missing 
    # in plans the response does not have data param so this will fail instead if returning a 
    #bad request error.

    if response is not None:
        if isinstance(response.data, list):
            response.data = {}
            response.data['type'] = exc.default_detail
            response.data['status'] = response.status_code
            response.data['errors'] = response.reason_phrase
            response.data['detail'] = str(exc)
        else:
            data = response.data
            response.data = {}
            errors = []
            for field, value in data.items():
                errors.append("{} : {}".format(field, " ".join(value)))
            
            response.data['type'] = exc.default_detail
            response.data['status'] = response.status_code
            response.data['errors'] = errors
            response.data['detail'] = str(exc)

    return response

