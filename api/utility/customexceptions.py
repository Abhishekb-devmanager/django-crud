from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

class BadRequest(APIException):
    status_code = 400
    default_detail = 'The request data is missing mandaory parameters.'
    default_code = 'bad_request'

class ValidationError(APIException):
    status_code = 400
    default_detail = 'The request data is invalid and not allowed.'
    default_code = 'bad_request'

class NotFound(APIException):
    status_code = 404
    default_detail = 'The requested resource does not exist.'
    default_code = 'Not Found'