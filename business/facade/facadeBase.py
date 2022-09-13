from abc import ABC, abstractmethod
import datetime
from common.constants.enums import Actions, Field, Entity, Reason
from common.exceptions.notFoundException import NotFoundException
from common.exceptions.notValidFlightException import NotValidFlightException
from common.exceptions.notValidOrderException import NotValidOrderException
from common.exceptions.invalidTokenException import InvalidTokenException
from common.exceptions.notValidLoginException import NotValidLoginException
from common.exceptions.systemException import FlightSystemException
from common.constants.settings import MinimumDate, MaximumDate ,\
    GENERAL_CLIENT_ERROR_MESSAGE, EMPTY_INPUT_CLIENT_MESSAGE, NOT_UNIQUE_CLIENT_MESSAGE, \
    LOGIN_FAILED_CLIENT_MESSAGE, RESOURCE_NOT_FOUND_MESSAGE, NOT_AUTHORIZED_MESSAGE
from common.exceptions.notValidInputException import NotVaildInputException
from common.exceptions.notUniqueException import NotUniqueException
from business.services.loggingService import FlightsLogger
from business.services.customerService import CustomerService
from business.services.airlineService import AirlineService
from business.services.loginService import LoginService
from business.services.ordersService import OrdersService
from dataAccess.FlightRepository import FilghtRepository
import logging

logger = FlightsLogger.get_instance().Logger


class FacadeBase:
    @abstractmethod
    def __init__(self, local_session):
        self.local_session = local_session
        self._repository = FilghtRepository(self.local_session)
        self._airlineService = AirlineService(self.local_session, self._repository)
        self._customerService = CustomerService(self.local_session, self._repository)
        self._ordersService = OrdersService(self.local_session, self._repository)
        self._loginService = LoginService(self.local_session, self._repository)

    def validate_token(self, identity_id, action_id):
        pass



    def get_all_flights(self):
        try:
            flights = self._airlineService.get_all_flights()
            return flights
        except Exception as exc:
            self.handle_exception(Actions.GET_ALL_FLIGHTS, exc)

    def get_flight_by_id(self, flight_id):
        try:
            flight = self._airlineService.get_flight_by_id(flight_id)
            return flight
        except Exception as exc:
            self.handle_exception(Actions.GET_FLIGHT_BY_ID, exc)

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, start_date, end_date):
        try:
            # self._airlineService.check_flight_params(origin_country_id, destination_country_id, start_date, end_date)
            parse_start_date = None
            if start_date is not None:
                parse_start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
            parse_end_date = None
            if end_date is not None:
                parse_end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
            flights = self._airlineService.get_flights_by_params(origin_country_id, destination_country_id,
                                                                 parse_start_date, parse_end_date)
            return flights
        except Exception as exc:
            self.handle_exception(Actions.GET_FLIGHT_BY_PARAMS, exc)

    def get_all_airlines(self):
        try:
            airlines = self._airlineService.get_all_airlines()
            return airlines
        except Exception as exc:
            self.handle_exception(Actions.GET_ALL_AIRLINES, exc)

    def get_airline_by_id(self, airline_id):
        try:
            airline = self._airlineService.get_airline_by_id(airline_id)
            if airline is None:
                raise NotFoundException('Airline Not Found', Entity.AIRLINE_COMPANY, airline_id)
            return airline
        except Exception as exc:
            self.handle_exception(Actions.GET_AIRLINE_BY_ID, exc)

    def get_airlines_by_parameters(self, country_id, name):
        try:
            airlines = self._airlineService.get_airlines_by_parameters(country_id, name)
            return airlines
        except Exception as exc:
            self.handle_exception(Actions.GET_AIRLINES_BY_PARAMS, exc)

    def get_all_countries(self):
        try:
            countries = self._airlineService.get_all_countries()
            return countries
        except Exception as exc:
            self.handle_exception(Actions.GET_ALL_COUNTRIES, exc)

    def get_country_by_id(self, country_id):
        try:
            country = self._airlineService.get_country_by_id(country_id)
            if country is None:
                raise NotFoundException('Country Not Found', Entity.COUNTRY, country_id)
            return country
        except Exception as exc:
            self.handle_exception(Actions.GET_COUNTRY_BY_ID, exc)

    def get_customer_by_id(self, customer_id):
        try:
            customer = self._customerService.get_customer_by_id(customer_id)
            if customer is None:
                raise NotFoundException('Customer Not Found', Entity.CUSTOMER, customer_id)
            return customer
        except Exception as exc:
            self.handle_exception(Actions.GET_CUSTOMER_BY_ID, exc)

    def create_user(self, user):
        try:
            # validate user fields
            LoginService.validate_new_user(user)
            # check unique user name
            exist_user = self._loginService.get_user_by_user_name(user.username)
            if exist_user is not None:
                raise NotUniqueException('User Name Already Exists', Actions.CREATE_NEW_USER, Field.USER_NAME,
                                     user.username)
            exist_email = self._loginService.get_user_by_email(user.email)
            if exist_email is not None:
                raise NotUniqueException('Email Already Exists', Actions.CREATE_NEW_USER, Field.USER_EMAIL,
                                     user.email)
            # create new user
            self._loginService.create_new_user(user)
        except Exception as exc:
            self.handle_exception(Actions.CREATE_NEW_USER, exc)

    def handle_exception(self, action, exception: Exception):
        # 1) error login
        if isinstance(exception, NotValidLoginException):
            # logger
            logger.log(logging.ERROR,
                       f'{str(exception)}, username={exception.user_name}, password={exception.password}')
            # outputs
            raise FlightSystemException(LOGIN_FAILED_CLIENT_MESSAGE, exception)

        # 2) NotVaildInput
        elif isinstance(exception, NotVaildInputException):
            # logger
            logger.log(logging.ERROR,
            f'{str(exception)}, cause={exception.cause}, field_name={exception.field_name}')
            # outputs
            raise FlightSystemException(EMPTY_INPUT_CLIENT_MESSAGE, exception)

        # 3) not unique values
        elif isinstance(exception, NotUniqueException):
            # logger
            logger.log(logging.ERROR,
            f'{str(exception)}, field_name={exception.field_name} reuqested_value={exception.reuqested_value}')
            # outputs
            raise FlightSystemException(NOT_UNIQUE_CLIENT_MESSAGE, exception)

        # 4) resource not found
        elif isinstance(exception, NotFoundException):
            # logger
            logger.log(logging.ERROR,
                       f'{str(exception)}, entity={exception.entity} entity_id={exception.entity_id}')
            # outputs
            raise FlightSystemException(RESOURCE_NOT_FOUND_MESSAGE, exception)

        # 5) invalid token (not authorized)
        elif isinstance(exception, InvalidTokenException):
            # logger
            logger.log(logging.ERROR,
                       f'{str(exception)}, action={exception.action}, token={exception.token},'
                       f' field_name={exception.field_name}, field_value={exception.field_value}')
            # outputs
            raise FlightSystemException(NOT_AUTHORIZED_MESSAGE, exception)

        # 6) error in ordering ticket --- send custom message
        elif isinstance(exception, NotValidOrderException):
            # logger
            logger.log(logging.INFO,
            f'{str(exception)}, cause={exception.cause}')
            # outputs
            raise FlightSystemException(str(exception), exception)

        # 7) error in flight
        elif isinstance(exception, NotValidFlightException):
            logger.log(logging.ERROR,
                       f'{str(exception)}, reason={exception.cause}')
            raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)

        # 8) other general exception
        else:  # PYTHON EXCEPTION - ALSO GENERAL MESSAGE ERROR
            # logger
            logger.log(logging.ERROR, f'{str(exception)}')
            # outputs
            raise FlightSystemException(GENERAL_CLIENT_ERROR_MESSAGE, exception)

    # added custom functions




