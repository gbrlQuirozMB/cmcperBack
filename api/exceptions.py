from rest_framework.exceptions import APIException, ValidationError


class Otro(APIException):
    status_code = 555
    default_detail = 'Algo muy especifico'
    default_code = 'error'


class CamposIncorrectos(ValidationError):
    default_code = 'error'

    def __init__(self, detail, status_code=400):
        response = {'detail': detail}
        self.detail = response
        self.status_code = status_code


class ResponseError(APIException):
    default_code = 'error'

    def __init__(self, detail, code):
        self.detail = detail
        self.status_code = code
