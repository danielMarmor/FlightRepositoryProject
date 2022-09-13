from business.facade.facadeBase import FacadeBase
from business.services.loginService import LoginService
from common.constants.enums import Actions, Reason, Field, UserRoles, Entity
from common.exceptions.systemException import FlightSystemException
from common.exceptions.notValidInputException import NotVaildInputException
from common.exceptions.notValidLoginException import NotValidLoginException
from common.exceptions.notUniqueException import NotUniqueException
from common.exceptions.notFoundException import NotFoundException
from common.constants.settings import GENERAL_CLIENT_ERROR_MESSAGE, NOT_UNIQUE_CLIENT_MESSAGE, \
    EMPTY_INPUT_CLIENT_MESSAGE, LOGIN_FAILED_CLIENT_MESSAGE
from business.services.loggingService import FlightsLogger
from business.facade.customerFacade import CustomerFacade
from business.facade.airlineFacade import AirlineFacade
from business.facade.administratorFacade import AdministratorFacade
from common.not_mapped.identityToken import IdentityToken
from common.not_mapped.UserDetails import UserDetails
import logging

logger = FlightsLogger.get_instance().Logger


class AnonymousFacade(FacadeBase):
    def __init__(self, local_session):
        super().__init__(local_session)

    def validate_token(self, identity_id, action_id):
        pass

    # anonymouse
    def login(self, username, password):
        try:
            LoginService.validate_login(username, password)
            user = self._loginService.login(username, password)
            facade = self.create_facade(user.user_role, user.username)
            token = facade.token
            identity = facade.get_details(token.identity_id)
            user_details = UserDetails(token, identity)
            return user_details
        except Exception as exc:
            self.handle_exception(Actions.LOGIN, exc)

    # create facade
    def create_facade(self, user_role_id, user_name):
        match user_role_id:
            case UserRoles.CUSTOMER:
                customer_facade = self.get_customer_facade(user_name, user_role_id)
                return customer_facade
            case UserRoles.AIRLINE:
                airlie_facade = self.get_airline_facade(user_name, user_role_id)
                return airlie_facade
            case UserRoles.ADMINISTATOR:
                administrator_facade = self.get_adminitrator_facade(user_name, user_role_id)
                return administrator_facade

    def get_customer_facade(self, username, userrole):
        customer = self._repository.get_customer_by_username(username)
        if customer is None:
            raise NotFoundException('Cusotmer Not Found', Entity.CUSTOMER, username)
        token = IdentityToken(username, userrole, customer.id)
        facade = CustomerFacade(self.local_session, token)
        return facade

    def get_airline_facade(self, username, userrole):
        airline = self._repository.get_airline_by_username(username)
        if airline is None:
            raise NotFoundException('Airline Not Found', Entity.AIRLINE_COMPANY, username)
        token = IdentityToken(username, userrole, airline.id)
        facade = AirlineFacade(self.local_session, token)
        return facade

    def get_adminitrator_facade(self,  username, userrole):
        administrator = self._repository.get_administrator_by_username(username)
        if administrator is None:
            raise NotFoundException('administrator Not Found', Entity.ADMINISTRATOR, username)
        token = IdentityToken(username, userrole, administrator.id)
        facade = AdministratorFacade(self.local_session, token)
        return facade

    # custom required operations - private methods -check it out!!!
    def get_user_by_user_name(self, username):
        user = self._loginService.get_user_by_user_name(username)
        return user

    def add_customer(self, customer, user):
        try:
            # CREATE USER
            user = user.adapt_str()
            customer.adapt_str()
            # OK - CREATE CUSTOMER
            self._loginService.validate_new_user(user)
            self._customerService.validate_customer(customer)
            self._customerService.add_customer(customer, user)
            facade = self.create_facade(user.user_role, user.username)
            token = facade.token
            identity = facade.get_details(token.identity_id)
            user_details = UserDetails(token, identity)
            return user_details
        except Exception as exc:
            self.handle_exception(Actions.ADD_CUSTOMER, exc)

    def add_airline(self, airline, user):
        # validate
        try:
            # CREATE USER
            user = user.adapt_str()
            airline.adapt_str()
            self._loginService.validate_new_user(user)
            self._airlineService.validate_airline(airline)
            self._airlineService.add_airline(airline, user)
            facade = self.create_facade(user.user_role, user.username)
            token = facade.token
            identity = facade.get_details(token.identity_id)
            user_details = UserDetails(token, identity)
            return user_details
        except Exception as exc:
            self.handle_exception(Actions.ADD_AIRLINE, exc)

    # FILTER EXCEPTION BEFORE SHOWING MESSAGE TO USER - RAISE ALWAYS FlightSystemException
    def handle_exception(self, action, exception: Exception):
        # first -check basefacede(super) actions
        super().handle_exception(action, exception)
        # match case by anonymusfacade actions
        # if isinstance(exception, NotVaildInputException):
        #     raise FlightSystemException(EMPTY_INPUT_CLIENT_MESSAGE, exception)
        #
        # elif isinstance(exception, NotValidLoginException):
        #     raise FlightSystemException(LOGIN_FAILED_CLIENT_MESSAGE, exception)
        #
        # elif isinstance(exception, NotFoundException):
        #     logger.log(logging.ERROR,
        #                f'{str(exception)}, entity={exception.entity} entity_id={exception.entity_id}')
        #     raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)
        #
        # elif isinstance(exception, NotUniqueException):
        #     logger.log(logging.ERROR,
        #         f'{str(exception)}, field_name={exception.field_name} reuqested_value={exception.reuqested_value}')
        #     raise FlightSystemException(NOT_UNIQUE_CLIENT_MESSAGE, exception)
        #
        # else:  # PYTHON EXCEPTION (NOT CUSTOMED)-  GENERAL MESSAGE ERROR
        #      logger.log(logging.ERROR, f'{str(exception)}')
        #      raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)

    def get_all_customers_users(self):
        try:
            users = self._loginService.get_all_customers_users()
            return users
        except Exception as exc:
            self.handle_exception(Actions.GET_ALL_USERS, exc)

    def get_tickets_by_username(self, email):
        try:
            user = self._loginService.get_user_by_email(email)
            if user is None:
                raise NotFoundException('User Not Found', Entity.USER, email)
            customer = self._customerService.get_customer_by_user_id(user.id)
            if customer is None:
                raise NotFoundException('Customer Not Found', Entity.CUSTOMER, user.id)
            customer_tickets = self._ordersService.get_tickets_by_customer(customer.id)
            return customer_tickets
        except Exception as exc:
            self.handle_exception(Actions.GET_TICKETS_BY_USER, exc)