from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    # if response is not None:
    #     response.data['status_code'] = response.status_code
    #     response.data['error'] = response.data['detail']
    if response is not None:
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