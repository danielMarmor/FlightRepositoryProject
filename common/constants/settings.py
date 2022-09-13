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
GENERAL_CLIENT_ERROR_MESSAGE = 'We couldnt complete your request. Please contact support'
NOT_UNIQUE_CLIENT_MESSAGE = 'One of the details you gave us allready exists in the system.' \
                            ' Check your data, or consult our support'
EMPTY_INPUT_CLIENT_MESSAGE = 'Please type valid inputs. One of your inputs is missing'
LOGIN_FAILED_CLIENT_MESSAGE = 'User name or password are incorrect !'
NOT_AUTHORIZED_MESSAGE = 'You Are Not Authorized To Commit This Operation. Please contact support'
RESOURCE_NOT_FOUND_MESSAGE = 'One of the resources you are trying to acsess not exists or not availiable. '\
    'Please contact support'
SCRIPTS_DELIMITER = '$EXCE SCRIPT'
