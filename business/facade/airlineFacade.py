from business.facade.facadeBase import FacadeBase
from common.exceptions.systemException import FlightSystemException
from common.constants.enums import Reason, Field, Actions, Entity
from common.constants.settings import GENERAL_CLIENT_ERROR_MESSAGE, NOT_UNIQUE_CLIENT_MESSAGE, \
    EMPTY_INPUT_CLIENT_MESSAGE
from common.exceptions.notValidInputException import NotVaildInputException
from common.exceptions.notFoundException import NotFoundException
from common.exceptions.notUniqueException import NotUniqueException
from business.services.loggingService import FlightsLogger
from common.not_mapped.identityToken import IdentityToken
from common.exceptions.invalidTokenException import InvalidTokenException
from business.services.airlineService import AirlineService
from common.exceptions.notValidFlightException import NotValidFlightException
from common.not_mapped.UserDetails import UserDetails
import logging

logger = FlightsLogger.get_instance().Logger


class AirlineFacade(FacadeBase):
    def __init__(self, local_session, token):
        super().__init__(local_session)
        self._token = token

    @property
    def token(self):
        return self._token

    def get_details(self, identity_id):
        airline = self.get_airline_by_id(identity_id)
        return airline

    def validate_token(self, airline_id, action_id):
        pass
        airline = self.get_airline_by_id(airline_id)
        if airline is None:
            raise NotFoundException('Airline Not Found', Entity.AIRLINE_COMPANY, airline_id)
        user = self._loginService.get_user_by_id(airline.user_id)
        if user is None:
            raise NotFoundException('User Not Found', Entity.USER, airline.user_id)
        if self._token is None:
            raise NotFoundException('Token Not Found', Entity.IDENTITY_TOKEN, airline.user_id)
        match_token = IdentityToken(user.username, user.user_role, airline_id)
        if match_token.identity_id != self._token.identity_id:
            raise InvalidTokenException('AirlineId Not Match Token Identity_Id', action_id,
                                        self._token, Field.AIRLINE_COMPANY_ID, match_token.identity_id)
        if match_token.user_name != self._token.user_name:
            raise InvalidTokenException('User_name Not Match Token User_name', action_id,
                                        self._token, Field.USER_NAME, match_token.user_name)
        if match_token.user_role_id != self._token.user_role_id:
            raise InvalidTokenException('User_role_id Not Match Token User_role_id', action_id,
                                        self._token, Field.USER_ROLE_ID, match_token.user_role_id)

    # flights
    def get_my_flights(self, airline_id):
        try:
            airline = self.get_airline_by_id(airline_id)
            self.validate_token(airline.id, Actions.GET_FLIGHT_BY_AIRLINE)
            flights = self._airlineService.get_flights_by_airline(airline.id)
            return flights
        except Exception as exc:
            self.handle_exception(Actions.GET_FLIGHT_BY_AIRLINE, exc)

    def update_airline(self, airline_id, airline, user):
        try:
            airline.adapt_str()
            airline_company = self.get_airline_by_id(airline_id)
            user_id = airline_company.user_id
            self.validate_token(airline_company.id, Actions.UPDATE_AIRLINE)
            self._loginService.validate_update_user(user_id, user)
            airline.id = airline_id
            airline.user_id = user_id
            self._airlineService.validate_airline(airline)
            self._airlineService.update_airline(user_id, user, airline_id, airline)
            upd_user = self._loginService.login(user.username, user.password)
            self._token = IdentityToken(upd_user.username, upd_user.user_role, airline_id)
            token =  self.token
            identity = self.get_details(token.identity_id)
            user_details = UserDetails(token, identity)
            return user_details
        except Exception as exc:
            self.handle_exception(Actions.UPDATE_AIRLINE, exc)

    def add_flight(self, flight):
        try:
            self._airlineService.validate_flight(flight)
            airline_company = self.get_airline_by_id(flight.airline_company_id)
            self.validate_token(airline_company.id, Actions.ADD_FLIGHT)
            self._airlineService.add_fligth(flight)
            return flight
        except Exception as exc:
            self.handle_exception(Actions.ADD_FLIGHT, exc)

    def update_flight(self, flight_id, flight):
        try:
            orig_flight = self.get_flight_by_id(flight_id)
            orig_airline_company = self.get_airline_by_id(orig_flight.airline_company_id)
            self.validate_token(orig_airline_company.id, Actions.UPDATE_FLIGHT)
            AirlineService.validate_flight(flight)
            self._airlineService.update_fligth(flight_id, flight)
        except Exception as exc:
            self.handle_exception(Actions.UPDATE_FLIGHT, exc)

    def remove_flight(self, flight_id):
        try:
            flight = self.get_flight_by_id(flight_id)
            airline_company = self.get_airline_by_id(flight.airline_company_id)
            self.validate_token(airline_company.id, Actions.REMOVE_FLIGHT)
            self._airlineService.remove_flight(flight_id)
        except Exception as exc:
            self.handle_exception(Actions.REMOVE_FLIGHT, exc)

    def get_tickets_by_flight(self, flight_id):
        tickets = self._ordersService.get_tickets_by_flight(flight_id)
        return tickets

    def handle_exception(self, action, exception: Exception):
        super().handle_exception(action, exception)
        # if isinstance(exception, InvalidTokenException):
        #     logger.log(logging.ERROR,
        #             f'{str(exception)}, action={exception.action}, token={exception.token},'
        #             f' field_name={exception.field_name}, field_value={exception.field_value}')
        #     raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)
        # elif isinstance(exception, NotVaildInputException):
        #     logger.log(logging.ERROR,
        #             f'{str(exception)}, cause={exception.cause}, field_name={exception.field_name}')
        #     raise FlightSystemException(EMPTY_INPUT_CLIENT_MESSAGE, exception)
        # elif isinstance(exception, NotUniqueException):
        #     logger.log(logging.ERROR,
        #             f'{str(exception)}, field_name={exception.field_name} reuqested_value={exception.reuqested_value}')
        #     raise FlightSystemException(NOT_UNIQUE_CLIENT_MESSAGE, exception)
        # elif isinstance(exception, NotFoundException):
        #     logger.log(logging.ERROR,
        #             f'{str(exception)}, entity={exception.entity} entity_id={exception.entity_id}')
        #     raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)
        # elif isinstance(exception, NotValidFlightException):
        #     logger.log(logging.ERROR,
        #             f'{str(exception)}, reason={exception.cause}')
        #     raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)
        # else:  # PYTHON EXCEPTION - ALSO GENERAL MESSAGE ERROR
        #     logger.log(logging.ERROR, f'{str(exception)}')
        #     raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)
