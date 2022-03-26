from business.facade.facadeBase import FacadeBase
from business.services.customerService import CustomerService
from common.exceptions.notFoundException import NotFoundException
from common.exceptions.notUniqueException import NotUniqueException
from common.exceptions.systemException import FlightSystemException
from common.constants.enums import Field, Actions, Reason, Entity
from common.exceptions.notValidInputException import NotVaildInputException
from common.constants.settings import EMPTY_INPUT_CLIENT_MESSAGE, GENERAL_CLIENT_ERROR_MESSAGE, \
    NOT_UNIQUE_CLIENT_MESSAGE
from business.services.loggingService import FlightsLogger
from common.exceptions.invalidTokenException import InvalidTokenException
from common.not_mapped.identityToken import IdentityToken
import logging

logger = FlightsLogger.get_instance().Logger


class AdministratorFacade(FacadeBase):
    def __init__(self, local_session, token):
        super().__init__(local_session)
        self._token = token

    def validate_token(self, administrator_id, action_id):
        administrator = self._airlineService.get_administrator_by_id(administrator_id)
        if administrator is None:
            raise NotFoundException('Aministrator Not Found', Entity.ADMINISTRATOR, administrator_id)
        user = self._loginService.get_user_by_id(administrator.user_id)
        if user is None:
            raise NotFoundException('User Not Found', Entity.USER, administrator.user_id)
        if self._token is None:
            raise NotFoundException('Token Not Found', Entity.IDENTITY_TOKEN, administrator.user_id)
        match_token = IdentityToken(user.username, user.user_role, administrator.id)
        if match_token.identity_id != self._token.identity_id:
            raise InvalidTokenException('AministratorId Not Match Token Identity_Id', action_id,
                                        self._token, Field.AIRLINE_COMPANY_ID, match_token.identity_id)
        if match_token.user_name != self._token.user_name:
            raise InvalidTokenException('User_name Not Match Token User_name', action_id,
                                        self._token, Field.USER_NAME, match_token.user_name)
        if match_token.user_role_id != self._token.user_role_id:
            raise InvalidTokenException('User_role_id Not Match Token User_role_id', action_id,
                                        self._token, Field.USER_ROLE_ID, match_token.user_role_id)

    # administrator
    def get_all_customers(self):
        try:
            customers = self._customerService.get_all_customers()
            return customers
        except Exception as exc:
            self.handle_exception(Actions.GET_ALL_CUSTOMERS, exc)

    def add_airline(self, airline, user):
        # validate
        try:
            # CREATE USER
            user = user.adapt_str()
            airline.adapt_str()
            self._loginService.validate_new_user(user)
            self._airlineService.validate_airline(airline)
            self._airlineService.add_airline(airline, user)
        except Exception as exc:
            self.handle_exception(Actions.ADD_AIRLINE, exc)

    # def add_airline(self, airline, user):
    #     # validate
    #     try:
    #         # CREATE USER
    #         user = user.adapt_str()
    #         self.create_user(user)
    #         airline.adapt_str()
    #         airline.user_id = user.id
    #         self._airlineService.validate_airline(airline)
    #         self._airlineService.add_airline(airline)
    #     except Exception as exc:
    #         self.handle_exception(Actions.ADD_AIRLINE, exc)

    def add_customer(self, customer, user):
        try:
            # CREATE USER
            user = user.adapt_str()
            customer.adapt_str()
            # OK - CREATE CUSTOMER
            self._loginService.validate_new_user(user)
            self._customerService.validate_customer(customer)
            self._customerService.add_customer(customer, user)
        except Exception as exc:
            self.handle_exception(Actions.ADD_CUSTOMER, exc)

    # def add_customer(self, customer, user):
    #     try:
    #         # CREATE USER
    #         user = user.adapt_str()
    #         self.create_user(user)
    #         customer.adapt_str()
    #         customer.user_id = user.id
    #         # OK - CREATE CUSTOMER
    #         self._customerService.validate_customer(customer)
    #         self._customerService.add_customer(customer)
    #     except Exception as exc:
    #         self.handle_exception(Actions.ADD_CUSTOMER, exc)

    def remove_airline(self, airline_id):
        try:
            airline = self.get_airline_by_id(airline_id)
            if airline is None:
                raise NotFoundException('Airline not Found', Entity.AIRLINE_COMPANY, airline_id)
            self._airlineService.remove_airline(airline_id)
        except Exception as exc:
            self.handle_exception(Actions.REMVOE_AIRLINE, exc)

    def remove_customer(self, customer_id):
        try:
            self._customerService.remove_customer(customer_id)
        except Exception as exc:
            self.handle_exception(Actions.REMOVE_CUSTOMER, exc)

    def add_administrator(self, administrator, user):
        # validate
        try:
            user = user.adapt_str()
            administrator.adapt_str()
            self._loginService.validate_new_user(user)
            self._airlineService.validate_administrator(administrator)
            self._airlineService.add_administrator(administrator, user)
        except Exception as exc:
            self.handle_exception(Actions.ADD_ADMINISTRATOR, exc)

    def remove_administrator(self, administrator_id):
        try:
            administrator = self._airlineService.get_administrator_by_id(administrator_id)
            if administrator is None:
                raise NotFoundException('Administrator Not Found!', Entity.ADMINISTRATOR, administrator_id)
            self.validate_token(administrator.id, Actions.REMOVE_ADMINISTRATOR)
            self._airlineService.remove_administrator(administrator_id)
        except Exception as exc:
            self.handle_exception(Actions.REMOVE_ADMINISTRATOR, exc)

    # additional functions
    def get_customer_by_id(self, customer_id):
        customer = self._customerService.get_customer_by_id(customer_id)
        return customer

    def get_administrator_by_id(self, administrator_id):
        administrator = self._airlineService.get_administrator_by_id(administrator_id)
        return administrator

    def handle_exception(self, action, exception: Exception):
        super().handle_exception(action, exception)
        if isinstance(exception, InvalidTokenException):
            logger.log(logging.ERROR,
                       f'{str(exception)}, action={exception.action}, token={exception.token},'
                       f' field_name={exception.field_name}, field_value={exception.field_value}')
            raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)
        elif isinstance(exception, NotVaildInputException):
            logger.log(logging.ERROR,
                       f'{str(exception)}, cause={exception.cause}, field_name={exception.field_name}')
            raise FlightSystemException(EMPTY_INPUT_CLIENT_MESSAGE, exception)
        elif isinstance(exception, NotUniqueException):
            logger.log(logging.ERROR,
                       f'{str(exception)}, field_name={exception.field_name} reuqested_value={exception.reuqested_value}')
            raise FlightSystemException(NOT_UNIQUE_CLIENT_MESSAGE, exception)
        elif isinstance(exception, NotFoundException):
            logger.log(logging.ERROR,
                       f'{str(exception)}, entity={exception.entity} entity_id={exception.entity_id}')
            raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)
        else:  # PYTHON EXCEPTION - ALSO GENERAL MESSAGE ERROR
            logger.log(logging.ERROR, f'{str(exception)}')
            raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)
