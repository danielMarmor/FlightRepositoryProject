import pytest
from common.constants.settings import USER_ROLE_ADMIN
from dataAccess.FlightRepository import FilghtRepository
from business.facade.anonymousFacade import *
from business.facade.customerFacade import CustomerFacade
from business.facade.administratorFacade import AdministratorFacade
from business.facade.airlineFacade import AirlineFacade
from business.services.loginService import *
from business.services.testService import TestService
from common.entities.User import User
from common.entities.Flight import Flight
from common.entities.AirlineCompany import AirlineCompany
from common.exceptions.notValidLoginException import NotValidLoginException
from common.exceptions.notUniqueException import NotUniqueException
from business.services.genericService import GenericService
from common.entities.db_config import local_session, create_all_entities, connection_string
from common.entities.db_conifg_procedured import load_db_scripts
from common.exceptions.notFoundException import NotFoundException
from common.entities.Customer import Customer
from common.exceptions.invalidTokenException import InvalidTokenException
from common.exceptions.notValidFlightException import NotValidFlightException
from datetime import datetime, timedelta


# abort process imedatly if not test environment
def validate_connection_string(conn_str):
    is_not_test = conn_str.find('Test') == -1
    if is_not_test:
        pytest.exit('Not Test Invironment DB ===> automaticaly Rejected all operations!')
        # /raise Exception('Not Test Invironment DB ===> automaticaly Rejected all operations!')


# anonymous facade
@pytest.fixture(scope='session', autouse=True)
def prepare():
    conn_str = connection_string
    validate_connection_string(conn_str)
    create_all_entities()
    load_db_scripts()


# test service == > for restore test database after every test unit
@pytest.fixture(scope='session', autouse=True)
def test_service():
    conn_str = connection_string
    validate_connection_string(conn_str)
    repository = FilghtRepository(local_session)
    service = TestService(local_session, repository)
    return service


# anonymous facade
@pytest.fixture(scope='session', autouse=True)
def facade():
    # conection string from db-config
    anonymous_facade = AnonymousFacade(local_session)
    return anonymous_facade


# restore test database
@pytest.fixture(scope='function', autouse=True)
def restore_test_database(test_service):
    test_service.restore_database()


# **************************************************************
# INHERITED FROM FACADE BASE
@pytest.fixture
def flight_id_exists():
    return 1


@pytest.fixture
def flight_id_not_exists():
    return 999


@pytest.fixture
def filghts_params():
    return {'origin_country': 1, 'dest_country': 2, 'date': '23/01/2022'}


@pytest.fixture
def airline_id_exists():
    return 1


@pytest.fixture
def airline_id_not_exists():
    return -999


@pytest.fixture
def airlines_params():
    return {'country_id': 1, 'name': 'Amer'}


@pytest.fixture
def country_id_exists():
    return 1


@pytest.fixture
def country_id_not_exists():
    return -999


# ...
def test_get_all_flights_positive(facade: AnonymousFacade):
    try:
        all_flights = facade.get_all_flights()
        assert True
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'


def test_get_flight_by_id_positive(facade: AnonymousFacade, flight_id_exists):
    try:
        flight = facade.get_flight_by_id(flight_id_exists)
        if not isinstance(flight, Flight):
            assert False, 'flight return no flight entity'
        if flight.id != flight_id_exists:
            assert False, f'return flight id {flight.id} not match input flight id {flight_id_exists}'
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised: {str(exc)}'


def test_get_flight_by_id_negative_notfound(facade :AnonymousFacade, flight_id_not_exists):
    try:
        flight = facade.get_flight_by_id(flight_id_not_exists)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.FLIGHT:
            assert False, f'test falied: not FLIGHT NotFoundException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_get_flights_by_parameters_positive(facade: AnonymousFacade, filghts_params):
    try:
        origin_country_id = filghts_params['origin_country']
        dest_country_id = filghts_params['dest_country']
        flight_date = filghts_params['date']
        flights_by_param = facade.get_flights_by_parameters(origin_country_id, dest_country_id, flight_date)
        assert True
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'


def test_get_all_airlines_positive(facade: AnonymousFacade):
    try:
        all_airlines = facade.get_all_airlines()
        assert True
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'


def test_get_airline_by_id_positive(facade, airline_id_exists):
    try:
        airline = facade.get_airline_by_id(airline_id_exists)
        if not isinstance(airline, AirlineCompany):
            assert False, 'airline return no AirlineCompany entity'
        if airline.id != airline_id_exists:
            assert False, f'return airline id {airline.id} not match input flight id {airline_id_exists}'
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised: {str(exc)}'


# flight not found
def test_get_airline_by_id_negative_notfound(facade, airline_id_not_exists):
    try:
        airline = facade.get_airline_by_id(airline_id_not_exists)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.AIRLINE_COMPANY:
            assert False, f'test falied: not AIRLINE_COMPANY NotFoundException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_get_airlines_by_parameters_positive(facade: AnonymousFacade, airlines_params):
    try:
        country_id = airlines_params['country_id']
        name = airlines_params['name']
        airlines_by_params = facade.get_airlines_by_parameters(country_id, name)
        assert True
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'


def test_get_all_countries_positive(facade: AnonymousFacade):
    try:
        countries = facade.get_all_countries()
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised: {str(exc)}'


def test_get_country_by_id_positive(facade: AnonymousFacade, country_id_exists):
    try:
        country = facade.get_country_by_id(country_id_exists)
        if country is None:
            assert False, f'Country is None!'
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised: {str(exc)}'


def test_get_country_by_id_neg_country_not_found(facade: AnonymousFacade, country_id_not_exists):
    try:
        country = facade.get_country_by_id(country_id_not_exists)
        if country is not None:
            assert False, f'Country should be None but returns not None!'
        assert True
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException'
        if inner.entity != Entity.COUNTRY:
            assert False, f'test falied: not COUNTRY NotFoundException'
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised: {str(exc)}'


# **************************************************************
# GET MY FILGHTS
@pytest.fixture
def exists_airline():
    return {'username': 'amair123', 'password': '019920098$3'}


@pytest.fixture
def get_my_flights_facade(facade: AnonymousFacade, exists_airline):
    airline_facade = facade.login(exists_airline['username'], exists_airline['password'])
    return airline_facade


def test_get_my_flights_positive(get_my_flights_facade: AirlineFacade, airline_id_exists):
    try:
        flights = get_my_flights_facade.get_my_flights(airline_id_exists)
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised: {str(exc)}'


def test_get_my_flights_neg_invalid_token(get_my_flights_facade: AirlineFacade):
    try:
        # INVALID TOKEN AIRLINE ID
        invalid_token_airline_id = 2
        flights = get_my_flights_facade.get_my_flights(invalid_token_airline_id)
        assert False, f'airline not exists, but there is no NotFoundException'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, InvalidTokenException):
            assert False, f'test falied: not InvalidTokenException'
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised: {str(exc)}'


def test_get_my_flights_neg_airline_not_exists(get_my_flights_facade: AirlineFacade, airline_id_not_exists):
    try:
        flights = get_my_flights_facade.get_my_flights(airline_id_not_exists)
        assert False, f'airline not exists, but there is no NotFoundException'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException'
        if inner.entity != Entity.AIRLINE_COMPANY:
            assert False, f'test falied: not AIRLINE_COMPANY NotFoundException'
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised: {str(exc)}'


# **********************************************
# UPDATE AIRLINE
@pytest.fixture
def update_airline_facade(facade: AnonymousFacade, exists_airline):
    airline_facade = facade.login(exists_airline['username'], exists_airline['password'])
    return airline_facade


@pytest.fixture
def updated_vailid_airline():
    return AirlineCompany(id=1, name='American Streams', country_id=1, user_id=5)


@pytest.fixture
def not_found_user_id():
    return -999


@pytest.fixture
def not_found_country_id():
    return -999


@pytest.fixture
def not_unique_airline_name():
    return 'British Airways'


def test_update_airline_positive(update_airline_facade: AirlineFacade, updated_vailid_airline):
    try:
        update_airline_facade.update_airline(updated_vailid_airline.id, updated_vailid_airline)
    except Exception as exc:
        print(f'exception is raised: {str(exc)}')
        assert False, f'exception is raised: {str(exc)}'
    # SUCCEDED :
    try:
        airline = update_airline_facade.get_airline_by_id(updated_vailid_airline.id)
        if airline is None:
            assert False, 'updated but returns airline None'
        if airline != updated_vailid_airline:
            assert False, 'updated but return airline is not identical'
        assert True
    except Exception as exc:
        print(f'exception is raised (but only on test code): {str(exc)}')
        assert False, f'exception is raised (but only on test code): {str(exc)}'


def test_update_airline_neg_invalid_token(update_airline_facade: AirlineFacade, updated_vailid_airline):
    # INVALID TOKEN # british airways
    updated_vailid_airline.id = 2
    try:
        update_airline_facade.update_airline(updated_vailid_airline.id, updated_vailid_airline)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, InvalidTokenException):
            assert False, f'test falied: not InvalidTokenException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# empty name
def test_update_airline_neg_empty_name(update_airline_facade: AirlineFacade, updated_vailid_airline):
    updated_vailid_airline.name = ''
    try:
        update_airline_facade.update_airline(updated_vailid_airline.id, updated_vailid_airline)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.AIRLINE_COMPANY_NAME:
            assert False, f'test falied: not EMPTY/AIRLINE_COMPANY_NAME NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# not_country_id
def test_update_airline_neg_empty_country_id(update_airline_facade: AirlineFacade, updated_vailid_airline):
    updated_vailid_airline.country_id = None
    try:
        update_airline_facade.update_airline(updated_vailid_airline.id, updated_vailid_airline)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.AIRLINE_COUNTRY_ID:
            assert False, f'test falied: not EMPTY/AIRLINE_COUNTRY_ID NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# not user_id
def test_update_airline_neg_empty_user_id(update_airline_facade: AirlineFacade, updated_vailid_airline):
    updated_vailid_airline.user_id = None
    try:
        update_airline_facade.update_airline(updated_vailid_airline.id, updated_vailid_airline)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.AIRLINE_USER_ID:
            assert False, f'test falied: not EMPTY/AIRLINE_USER_ID NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# invalid name
def test_update_airline_neg_name_too_long(update_airline_facade: AirlineFacade, updated_vailid_airline):
    updated_vailid_airline.name = 'A' * (AirlineCompany.MAX_NAME + 1)
    try:
        update_airline_facade.update_airline(updated_vailid_airline.id, updated_vailid_airline)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.TOO_LONG or inner.field_name != Field.AIRLINE_COMPANY_NAME:
            assert False, f'test falied: not TOO_LONG/AIRLINE_COMPANY_NAME NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# not exists_country_id
def test_update_airline_neg_not_exists_country_id(update_airline_facade: AirlineFacade, updated_vailid_airline, not_found_country_id):
    updated_vailid_airline.country_id = not_found_country_id
    try:
        update_airline_facade.update_airline(updated_vailid_airline.id, updated_vailid_airline)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.COUNTRY:
            assert False, f'test falied: not COUNTRY NotFoundException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# not exists_user_id
def test_update_airline_neg_not_exists_user_id(update_airline_facade: AirlineFacade, updated_vailid_airline, not_found_user_id):
    updated_vailid_airline.user_id = not_found_user_id
    try:
        update_airline_facade.update_airline(updated_vailid_airline.id, updated_vailid_airline)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.USER:
            assert False, f'test falied: not USER NotFoundException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# allready exists by name
def test_update_airline_neg_not_unique_name(update_airline_facade: AirlineFacade, updated_vailid_airline, not_unique_airline_name):
    updated_vailid_airline.name = not_unique_airline_name
    try:
        update_airline_facade.update_airline(updated_vailid_airline.id, updated_vailid_airline)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotUniqueException):
            assert False, f'test falied: not NotUniqueException exception: {str(inner)}'
        if inner.field_name != Field.AIRLINE_COMPANY_NAME:
            assert False, f'test falied: not AIRLINE_COMPANY_NAME NotUniqueException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# *********************************
# ADD FLIGHT
# UPDATE AIRLINE
@pytest.fixture
def add_flight_facade(facade: AnonymousFacade, exists_airline):
    add_flight_facade = facade.login(exists_airline['username'], exists_airline['password'])
    return add_flight_facade


@pytest.fixture
def new_valid_flight():
    return Flight(airline_company_id=1,
                  origin_country_id=1,
                  destination_country_id=2,
                  departure_time=datetime(2022, 1, 18, 12, 0, 0),
                  landing_time=datetime(2022, 1, 18, 23, 0, 0),
                  remaining_tickets=100)


def test_add_flight_positive(add_flight_facade: AirlineFacade, new_valid_flight):
    try:
        add_flight_facade.add_flight(new_valid_flight)
    except Exception as exc:
        print(f'exception is raised: {str(exc)}')
        assert False, f'exception is raised: {str(exc)}'
    # SUCCEDED :
    try:
        fligth = add_flight_facade.get_flight_by_id(new_valid_flight.id)
        if fligth is None:
            assert False, 'inserted but returns fligth None'
        if fligth != new_valid_flight:
            assert False, 'inserted but return fligth is not identical'
        assert True
    except Exception as exc:
        print(f'exception is raised (but only on test code): {str(exc)}')
        assert False, f'exception is raised (but only on test code): {str(exc)}'


def test_add_flight_neg_invalid_token(add_flight_facade: AirlineFacade, new_valid_flight: Flight):
    # INVALID TOKEN AIRLINE COMPANY ID = 2 (BRIT AIRWAYS)
    new_valid_flight.airline_company_id = 2
    try:
        add_flight_facade.add_flight(new_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, InvalidTokenException):
            assert False, f'test falied: not InvalidTokenException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_flight_neg_empty_airline_id(add_flight_facade: AirlineFacade, new_valid_flight: Flight):
    new_valid_flight.airline_company_id = None
    try:
        add_flight_facade.add_flight(new_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.FLIGHT_AIRLINE_ID:
            assert False, f'test falied: not EMPTY/FLIGHT_AIRLINE_ID NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# origin_country_id empty
def test_add_flight_neg_empty_origin_country_id(add_flight_facade: AirlineFacade, new_valid_flight: Flight):
    new_valid_flight.origin_country_id = None
    try:
        add_flight_facade.add_flight(new_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.FLIGHT_ORIGIN_COUNTRY_ID:
            assert False, f'test falied: not EMPTY/FLIGHT_ORIGIN_COUNTRY_ID NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# destination_country_id empty
def test_add_flight_neg_empty_dest_country_id(add_flight_facade: AirlineFacade, new_valid_flight: Flight):
    new_valid_flight.destination_country_id = None
    try:
        add_flight_facade.add_flight(new_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.FLIGHT_DEST_COUNTRY_ID:
            assert False, f'test falied: not EMPTY/FLIGHT_DEST_COUNTRY_ID NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# departure_time empty
def test_add_flight_neg_empty_departure_date(add_flight_facade: AirlineFacade, new_valid_flight: Flight):
    new_valid_flight.departure_time = None
    try:
        add_flight_facade.add_flight(new_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.FLIGHT_DEPARTURE_DATE:
            assert False, f'test falied: not EMPTY/FLIGHT_DEPARTURE_DATE NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# landing_time empty
def test_add_flight_neg_empty_landing_date(add_flight_facade: AirlineFacade, new_valid_flight: Flight):
    new_valid_flight.landing_time = None
    try:
        add_flight_facade.add_flight(new_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.FLIGHT_LANDING_DATE:
            assert False, f'test falied: not EMPTY/FLIGHT_LANDING_DATE NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# departure after landing times
def test_add_flight_neg_times_mismatch(add_flight_facade: AirlineFacade, new_valid_flight: Flight):
    new_valid_flight.departure_time = new_valid_flight.landing_time + timedelta(1)
    try:
        add_flight_facade.add_flight(new_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotValidFlightException):
            assert False, f'test falied: not NotValidFlightException exception: {str(inner)}'
        if inner.cause != Reason.DEPARTURE_LANDING_MISMATCH:
            assert False, f'test falied: not DEPARTURE_LANDING_MISMATCH NotValidFlightException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# remaining_tickets negative
def test_add_flight_neg_negative_tickets(add_flight_facade: AirlineFacade, new_valid_flight: Flight):
    new_valid_flight.remaining_tickets = 0
    try:
        add_flight_facade.add_flight(new_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotValidFlightException):
            assert False, f'test falied: not NotValidFlightException exception: {str(inner)}'
        if inner.cause != Reason.REMAING_TICKETS_INVALID:
            assert False, f'test falied: not REMAING_TICKETS_INVALID NotValidFlightException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# *******************************************
#  UPDATE FLIGHT
@pytest.fixture
def update_flight_facade(facade: AnonymousFacade, exists_airline):
    airline_facade = facade.login(exists_airline['username'], exists_airline['password'])
    return airline_facade


@pytest.fixture
def updated_valid_flight():
    return Flight(id=4,
                  airline_company_id=1,
                  origin_country_id=1,
                  destination_country_id=2,
                  departure_time=datetime(2022, 1, 14, 12, 0, 0),
                  landing_time=datetime(2022, 1, 14, 21, 0, 0),
                  remaining_tickets=1)


def test_update_flight_positive(update_flight_facade: AirlineFacade, updated_valid_flight):
    try:
        update_flight_facade.update_flight(updated_valid_flight.id, updated_valid_flight)
    except Exception as exc:
        print(f'exception is raised: {str(exc)}')
        assert False, f'exception is raised: {str(exc)}'
    # SUCCEDED :
    try:
        fligth = update_flight_facade.get_flight_by_id(updated_valid_flight.id)
        if fligth is None:
            assert False, 'inserted but returns fligth None'
        if fligth != updated_valid_flight:
            assert False, 'inserted but return fligth is not identical'
        assert True
    except Exception as exc:
        print(f'exception is raised (but only on test code): {str(exc)}')
        assert False, f'exception is raised (but only on test code): {str(exc)}'


def test_update_flight_neg_invalid_token(update_flight_facade: AirlineFacade, updated_valid_flight: Flight):
    try:
        # INVALID TOKEN
        updated_valid_flight.id = 7
        update_flight_facade.update_flight(updated_valid_flight.id, updated_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, InvalidTokenException):
            assert False, f'test falied: not InvalidTokenException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# airline_company_id empty
def test_update_flight_neg_empty_airline_id(update_flight_facade: AirlineFacade, updated_valid_flight: Flight):
    updated_valid_flight.airline_company_id = None
    try:
        update_flight_facade.update_flight(updated_valid_flight.id, updated_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.FLIGHT_AIRLINE_ID:
            assert False, f'test falied: not EMPTY/FLIGHT_AIRLINE_ID NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# origin_country_id empty
def test_update_flight_neg_empty_origin_country_id(update_flight_facade: AirlineFacade, updated_valid_flight: Flight):
    updated_valid_flight.origin_country_id = None
    try:
        update_flight_facade.update_flight(updated_valid_flight.id, updated_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.FLIGHT_ORIGIN_COUNTRY_ID:
            assert False, f'test falied: not EMPTY/FLIGHT_ORIGIN_COUNTRY_ID NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# destination_country_id empty
def test_update_flight_neg_empty_dest_country_id(update_flight_facade: AirlineFacade, updated_valid_flight: Flight):
    updated_valid_flight.destination_country_id = None
    try:
        update_flight_facade.update_flight(updated_valid_flight.id, updated_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.FLIGHT_DEST_COUNTRY_ID:
            assert False, f'test falied: not EMPTY/FLIGHT_DEST_COUNTRY_ID NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# departure_time empty
def test_update_flight_neg_empty_departure_date(update_flight_facade: AirlineFacade, updated_valid_flight: Flight):
    updated_valid_flight.departure_time = None
    try:
        update_flight_facade.update_flight(updated_valid_flight.id, updated_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.FLIGHT_DEPARTURE_DATE:
            assert False, f'test falied: not EMPTY/FLIGHT_DEPARTURE_DATE NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# landing_time empty
def test_update_flight_neg_empty_landing_date(update_flight_facade: AirlineFacade, updated_valid_flight: Flight):
    updated_valid_flight.landing_time = None
    try:
        update_flight_facade.update_flight(updated_valid_flight.id, updated_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.FLIGHT_LANDING_DATE:
            assert False, f'test falied: not EMPTY/FLIGHT_LANDING_DATE NotVaildInputException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# departure after landing times
def test_update_flight_neg_times_mismatch(update_flight_facade: AirlineFacade, updated_valid_flight: Flight):
    updated_valid_flight.departure_time = updated_valid_flight.landing_time + timedelta(1)
    try:
        update_flight_facade.update_flight(updated_valid_flight.id, updated_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotValidFlightException):
            assert False, f'test falied: not NotValidFlightException exception: {str(inner)}'
        if inner.cause != Reason.DEPARTURE_LANDING_MISMATCH:
            assert False, f'test falied: not DEPARTURE_LANDING_MISMATCH NotValidFlightException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# remaining_tickets negative
def test_update_flight_neg_negative_tickets(update_flight_facade: AirlineFacade, updated_valid_flight: Flight):
    updated_valid_flight.remaining_tickets = 0
    try:
        update_flight_facade.update_flight(updated_valid_flight.id, updated_valid_flight)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotValidFlightException):
            assert False, f'test falied: not NotValidFlightException exception: {str(inner)}'
        if inner.cause != Reason.REMAING_TICKETS_INVALID:
            assert False, f'test falied: not REMAING_TICKETS_INVALID NotValidFlightException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# *******************************************
# REMOVE FLIGHT
@pytest.fixture
def remove_flight_facade(facade: AnonymousFacade, exists_airline):
    airline_facade = facade.login(exists_airline['username'], exists_airline['password'])
    return airline_facade


@pytest.fixture
def flight_id_to_remove():
    return 1


@pytest.fixture
def invalid_token_fligth_to_remove():
    return 7  # BRIT AIRWAYS


@pytest.fixture
def not_exsits_flight_id():
    return -999


def test_remove_flight_positive(remove_flight_facade: AirlineFacade, flight_id_to_remove):
    try:
        remove_flight_facade.remove_flight(flight_id_to_remove)
        assert True
        # flight = remove_flight_facade.get_flight_by_id(flight_id_to_remove)
    except Exception as exc:
        print(f'exception is raised: {str(exc)}')
        assert False, f'exception is raised: {str(exc)}'


def test_remove_flight_neg_invalid_token(remove_flight_facade: AirlineFacade, invalid_token_fligth_to_remove):
    try:
        remove_flight_facade.remove_flight(invalid_token_fligth_to_remove)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, InvalidTokenException):
            assert False, f'test falied: not InvalidTokenException exception: {str(inner)}'
        assert True


def test_remove_flight_neg_flight_not_found(remove_flight_facade: AirlineFacade, flight_id_not_exists):
    try:
        remove_flight_facade.remove_flight(flight_id_not_exists)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.FLIGHT:
            assert False, f'test falied: not FLIGHT NotFoundException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'

