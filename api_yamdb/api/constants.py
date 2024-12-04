NAME_STRING_LENGTH = 255
STRING_SHOW = 30
SLUG_LENGTH = 50
NAME_TITLE_LENGTH = 100

USERNAME_REGEX = r'\bme\b'

CONFIRMATION_CODE_LENGTH = 10
CONFIRMATION_CODE_REGEX = r'^[A-Z\d]{%d}$' % CONFIRMATION_CODE_LENGTH
CONFIRMATION_EMAIL_BODY = 'confirmation_code_email_body.txt'
CONFIRMATION_EMAIL_SUBJECT = 'confirmation_code_email_subject.txt'
DOUBLE_REVIEW_ERROR = 'Можно оставлять только один отзыв на одно произведение.'

MIN_SCORE_VALUE = 1
MAX_SCORE_VALUE = 10
SCORE_VALIDATION_ERROR = ('Оценка {score} не соответствует диапазону от '
                          f'{MIN_SCORE_VALUE} до {MAX_SCORE_VALUE}')

USERNAME_INVALID = 'me'
USERNAME_LENGTH = 150
PASSWORD_LENGTH = 128
