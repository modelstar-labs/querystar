class BaseQueryStarException(Exception):
    """Base Exception raised for HTTP errors.

    Attributes:
        message     : Message of the error.

    """

    pass


class BadRequestException(BaseQueryStarException):
    # 400: General bad request with invalid parameters and/or values passed.
    # Message: Bad Request: Please make modifications to the request before pinging the server again.

    def __init__(self, context: str = None):
        self.status_code = 400
        self.message = 'Bad/Invalid Request: Please make modifications.\n Context: {context}'


class UnauthorizedException(BaseQueryStarException):
    # 403: Unauthorized request
    # Message: Invalid or expired authorization token.

    def __init__(self, context: str = None):
        self.status_code = 403
        self.message = 'Unauthorized request: You do not have a valid access token or permission to make the request.'
