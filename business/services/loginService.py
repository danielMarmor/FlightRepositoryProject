from common.entities.User import User
from common.constants.settings import EMPTY
from common.exceptions.notValidLoginException import NotValidLoginException
from common.constants.enums import Reason, Field
from common.constants.settings import USERNANE_MAX_LENGTH, PASSWORD_MIN_LENGHT, PASSWORD_MAX_LENGTH, EMAIL_MAX_LENGTH
from common.exceptions.notValidInputException import NotVaildInputException
from common.exceptions.notUniqueException import NotUniqueException
from common.constants.enums import Actions, Field
class LoginService:
    def __init__(self, local_session,  repository):
        self._repository = repository

    @staticmethod
    def validate_login(username, password):
        # validate user not empty
        if username.strip() == EMPTY:
            raise NotVaildInputException('User Name Empty', Reason.EMPTY, Field.USER_NAME)
        # validate password not empty
        if password.strip() == EMPTY:
            raise NotVaildInputException('User Name Empty', Reason.EMPTY, Field.USER_PASSWORD)
        pass

    def login(self, usrname, pssword):
        login_filter = (lambda query: query.filter(User.username == usrname, User.password == pssword))
        login_user_entries = self._repository.get_all_by_condition(User, login_filter)
        if len(login_user_entries) == 0:
            raise NotValidLoginException('User Not found by user-password match', usrname, pssword)
        login_user = login_user_entries[0]
        return login_user

    def create_new_user(self, new_user):
        # user = GenericService.get_strip_data(new_user)
        self._repository.add(new_user)
        # self._repository.commit()

    def validate_new_user(self, user):
        self.username_validation(user.username)
        self.password_validation(user.password)
        self.email_validation(user.email)

    def username_validation(self, username: str):
        username = username.strip()
        if username == EMPTY:
            raise NotVaildInputException('User Is Empty', Reason.EMPTY, Field.USER_NAME)
        is_too_long = len(username) > USERNANE_MAX_LENGTH
        if is_too_long:
            raise NotVaildInputException(f'User Name too long : Must be not bigger than {USERNANE_MAX_LENGTH} letters',
                                         Reason.TOO_LONG, Field.USER_NAME)
        unique_user_cond = (lambda query: query.filter(User.username == username))
        unique_user = self._repository.get_all_by_condition(User, unique_user_cond)
        if len(unique_user) > 0:
            raise NotUniqueException('Not Unique User Name', Actions.CREATE_NEW_USER, Field.USER_NAME, username)

    def password_validation(self, password: str):
        password = password.strip()
        if password == EMPTY:
            raise NotVaildInputException('Password Is Empty', Reason.EMPTY, Field.USER_PASSWORD)
        is_short = len(password) < PASSWORD_MIN_LENGHT
        if is_short:
            raise NotVaildInputException(f'Password too short : Must be at least {PASSWORD_MIN_LENGHT} letters!',
                                         Reason.TOO_SHORT, Field.USER_PASSWORD)
        is_long = len(password) > PASSWORD_MAX_LENGTH
        if is_long:
            raise NotVaildInputException(f'Password too long : Must be at least {PASSWORD_MAX_LENGTH} letters!',
                                         Reason.TOO_LONG, Field.USER_PASSWORD)

    @staticmethod
    def password_resembles_validaion(password: str):
        pass

    def email_validation(self, email: str):
        email = email.strip()
        if email == EMPTY:
            raise NotVaildInputException('Email Is Empty', Reason.EMPTY, Field.USER_EMAIL)
        is_too_long = len(email) > EMAIL_MAX_LENGTH
        if is_too_long:
            raise NotVaildInputException(f'Email too long : Must be at least {EMAIL_MAX_LENGTH} letters!',
                                         Reason.TOO_LONG, Field.USER_EMAIL)
        unique_email_cond = (lambda query: query.filter(User.email == email))
        unique_user = self._repository.get_all_by_condition(User, unique_email_cond)
        if len(unique_user) > 0:
            raise NotUniqueException('Not Unique Email', Actions.CREATE_NEW_USER, Field.USER_EMAIL, email)

    # custom function -- NEED TO BE PRIVATE === CHECK IT OUT !!!
    def get_user_by_user_name(self, user_name):
        user_name_filter = (lambda query: query.filter(User.username == user_name))
        user_name_entries = self._repository.get_all_by_condition(User, user_name_filter)
        if len(user_name_entries) == 0:
            return None
        user = user_name_entries[0]
        return user

    def get_user_by_email(self, email):
        email_filter = (lambda query: query.filter(User.email == email))
        user_name_entries = self._repository.get_all_by_condition(User, email_filter)
        if len(user_name_entries) == 0:
            return None
        user = user_name_entries[0]
        return user

    def get_user_by_id(self, user_id):
        user_id_filter = (lambda query: query.filter(User.id == user_id))
        user_id_entries = self._repository.get_all_by_condition(User, user_id_filter)
        if len(user_id_entries) == 0:
            return None
        user = user_id_entries[0]
        return user









