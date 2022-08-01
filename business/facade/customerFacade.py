from business.facade.facadeBase import FacadeBase
from common.constants.enums import Field, Reason, Entity, Actions
from common.exceptions.notValidInputException import NotVaildInputException
from common.exceptions.systemException import FlightSystemException
from common.exceptions.notUniqueException import NotUniqueException
from common.exceptions.notFoundException import NotFoundException
from common.exceptions.notValidOrderException import NotValidOrderException
from common.constants.settings import GENERAL_CLIENT_ERROR_MESSAGE, NOT_UNIQUE_CLIENT_MESSAGE, \
    EMPTY_INPUT_CLIENT_MESSAGE, LOGIN_FAILED_CLIENT_MESSAGE
from business.services.loggingService import FlightsLogger
from common.not_mapped.identityToken import IdentityToken
from common.exceptions.invalidTokenException import InvalidTokenException
import logging

logger = FlightsLogger.get_instance().Logger


class CustomerFacade(FacadeBase):
    def __init__(self, local_session, token):
        super().__init__(local_session)
        self._token = token

    @property
    def token(self):
        return self._token

    def validate_token(self, customer_id, action_id):
        customer = self._customerService.get_customer_by_id(customer_id)
        if customer is None:
            raise NotFoundException('Customer Not Found', Entity.CUSTOMER, customer_id)
        user = self._loginService.get_user_by_id(customer.user_id)
        if user is None:
            raise NotFoundException('User Not Found', Entity.USER, customer.user_id)
        if self.token is None:
            raise NotFoundException('Token Not Found', Entity.IDENTITY_TOKEN, customer.user_id)
        match_token = IdentityToken(user.username, user.user_role, customer_id)
        if match_token.user_name != self.token.user_name:
            raise InvalidTokenException('User_name Not Match Token User_name', action_id,
                                        self.token, Field.USER_NAME, match_token.user_name)
        if match_token.user_role_id != self.token.user_role_id:
            raise InvalidTokenException('User_role_id Not Match Token User_role_id', action_id,
                                        self.token, Field.USER_ROLE_ID, match_token.user_role_id)
        if match_token.identity_id != self.token.identity_id:
            raise InvalidTokenException('CustomerId Not Match Token Identity_Id', action_id,
                                        self.token, Field.CUSTOMER_ID, match_token.identity_id)

    # customer
    def update_customer(self, customer_id, customer, user):
        try:
            customer.adapt_str()
            exist_customer = self.get_customer_by_id(customer_id)
            if exist_customer is None:
                raise NotFoundException('Customer Not Found', Entity.CUSTOMER, customer_id)
            user_id = exist_customer.user_id
            customer.id = customer_id
            customer.user_id = user_id
            self.validate_token(customer_id, Actions.UPDATE_CUSTOMER)
            self._loginService.validate_update_user(user_id, user)
            self._customerService.validate_customer(customer)
            self._customerService.update_customer(user_id, user, customer_id, customer)
            upd_user = self._loginService.login(user.username, user.password)
            self._token = IdentityToken(upd_user.username, upd_user.user_role, customer_id)
            return self.token
        except Exception as exc:
            self.handle_exception(Actions.UPDATE_CUSTOMER, exc)

    def add_ticket(self, ticket):
        try:
            # check flight
            flight = self.get_flight_by_id(ticket.flight_id)
            if flight is None:
                raise NotFoundException('Flight Not Found', Entity.FLIGHT, ticket.flight_id)
            # check customer
            customer = self._customerService.get_customer_by_id(ticket.customer_id)
            if customer is None:
                raise NotFoundException('Customer Not Found', Entity.CUSTOMER, ticket.customer_id)
            # check token
            self.validate_token(ticket.customer_id, Actions.ADD_TICKET)
            # check order
            self._ordersService.check_order(flight, customer)
            # add tickets and #  remove ticket from flight remaing tickets
            self._ordersService.add_ticket(ticket, flight)
            return ticket
        except Exception as exc:
            self.handle_exception(Actions.ADD_TICKET, exc)

    def remove_ticket(self, ticket_id):
        try:
            # check if ticket exists
            ticket = self.get_ticket_by_id(ticket_id)
            if ticket is None:
                raise NotFoundException('Ticket Not Found!', Entity.TICKET, ticket_id)
            # check token - match with  ticket.customer_id
            self.validate_token(ticket.customer_id,  Actions.REMOVE_TICKET)
            flight = self.get_flight_by_id(ticket.flight_id)
            if flight is None:
                raise NotFoundException('Fligth Not Found!', Entity.FLIGHT, ticket.flight_id)
            # check cancel order
            self._ordersService.check_cancel_order(ticket)
            # remove ticket # add ticket to flight remaing tickets
            self._ordersService.remove_ticket(ticket_id, flight)
        except Exception as exc:
            self.handle_exception(Actions.REMOVE_TICKET, exc)

    def get_my_tickets(self, customer_id):
        try:
            customer = self._customerService.get_customer_by_id(customer_id)
            if customer is None:
                raise NotFoundException('Customer Not Found', Entity.CUSTOMER, customer_id)
            self.validate_token(customer_id, Actions.GET_TICKETS_BY_CUSTOMER)
            customer_tickets = self._ordersService.get_tickets_by_customer(customer_id)
            return customer_tickets
        except Exception as exc:
            self.handle_exception(Actions.GET_TICKETS_BY_CUSTOMER, exc)

    # added custom functions
    def get_customer_by_id(self, customer_id):
        customer = self._customerService.get_customer_by_id(customer_id)
        return customer

    def get_ticket_by_id(self, ticket_id):
        ticket = self._ordersService.get_ticket_by_id(ticket_id)
        return ticket

    def get_flights_by_customer(self, customer_id):
        customer_flights = self._customerService.get_flights_by_customer(customer_id)
        return customer_flights

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
        elif isinstance(exception, NotValidOrderException):
            logger.log(logging.INFO,
            f'{str(exception)}, cause={exception.cause}')
            raise FlightSystemException(str(exception), exception)
        else:  # PYTHON EXCEPTION - ALSO GENERAL MESSAGE ERROR
            logger.log(logging.ERROR, f'{str(exception)}')
            raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)

