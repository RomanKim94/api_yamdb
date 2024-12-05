NAME_STRING_LENGTH = 255
STRING_SHOW = 30
SLUG_LENGTH = 50
NAME_TITLE_LENGTH = 100

CONFIRMATION_CODE_ERROR = 'Некоректный код подтверждения.'
DOUBLE_REVIEW_ERROR = 'Можно оставлять только один отзыв на одно произведение.'

MIN_SCORE_VALUE = 1
MAX_SCORE_VALUE = 10


class HTTPMethod:
    """Класс с константами HTTP методов."""

    CONNECT = "CONNECT"
    DELETE = "DELETE"
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"
