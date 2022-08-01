from common.constants.enums import *
import datetime
# general
EMPTY = ''

# login
USER_ROLE_ADMIN = UserRoles.ADMINISTATOR
CUSTOMER_USER_ROLE = UserRoles.CUSTOMER
AIRLINE_USER_ROLE = UserRoles.AIRLINE
PASSWORD_MIN_LENGHT = 6
USERNANE_MAX_LENGTH = 20
PASSWORD_MAX_LENGTH = 20
EMAIL_MAX_LENGTH = 50

# dates
MinimumDate = datetime.datetime(1, 1, 1)
MaximumDate = datetime.datetime(9999, 12, 31)

# messages
GENERAL_CLIENT_ERROR_MESSAGE = 'We couldnt complete your request. please contact support'
NOT_UNIQUE_CLIENT_MESSAGE = 'One of the details you gave us allready exists in system.' \
                            ' check your data, or consult our support'
EMPTY_INPUT_CLIENT_MESSAGE = 'Please type valid inputs. one of your inputs is missing'
LOGIN_FAILED_CLIENT_MESSAGE= 'User Name or password are inncerect'

SCRIPTS_DELIMITER = '$EXCE SCRIPT'
