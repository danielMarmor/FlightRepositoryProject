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
from common.entities.Ticket import Ticket
from common.exceptions.notValidOrderException import NotValidOrderException
from common.exceptions.invalidTokenException import InvalidTokenException


# abort process imedatly if not test environment
def validate_connection_string(conn_str):
    is_not_test = conn_str.find('Test') == -1
    if is_not_test:
        pytest.exit('Not Test Invironment DB ===> automaticaly Rejected all operations!')
        # /raise Exception('Not Test Invironment DB ===> automaticaly Rejected all operations!')


# prepare
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


@pytest.fixture
def add_ticket_customer():
    return {'username': 'Stav1221', 'password': '8765432X'}


@pytest.fixture
def add_ticket_facade(facade: AnonymousFacade, add_ticket_customer):
    customer_facade = facade.login(add_ticket_customer['username'], add_ticket_customer['password'])
    return customer_facade


# restore test database
@pytest.fixture(scope='function', autouse=True)
def restore_test_database(test_service):
    test_service.restore_database()



# **************************************************************
pytest.fixture
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


def test_country_by_id_positive(facade: AnonymousFacade, country_id_exists):
    try:
        country = facade.get_country_by_id(country_id_exists)
        if country is None:
            assert False, f'Country is None!'
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised: {str(exc)}'


def test_country_by_id_neg_country_not_found(facade: AnonymousFacade, country_id_not_exists):
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
#  UPDATE CUSTOMER
@pytest.fixture(scope='session', autouse=True)
def exists_customer_user():
    return {'username': 'Daniel1221', 'password': '12345678'}


@pytest.fixture(scope='session', autouse=True)
def update_customer_facade(facade: AnonymousFacade, exists_customer_user):
    customer_facade = facade.login(exists_customer_user['username'], exists_customer_user['password'])
    return customer_facade


@pytest.fixture
def update_customer_valid():
    return Customer(id=1,
                    first_name='Daniel',
                    last_name='Marmor',
                    address='Givat Narkisiot 16 K.motzkin',
                    phone_number='   0543675402',
                    credit_card_number='1099-1111-2314-1234',
                    user_id=1)


@pytest.fixture
def update_customer_not_exists():
    return Customer(id=0,
                    first_name='Daniel',
                    last_name='Marmor',
                    address='Ben tzvi 3 K.motzkin',
                    phone_number='0523335402',
                    credit_card_number='1070-1111-2314-1234',
                    user_id=1)


@pytest.fixture
def exist_phone():
    return '0543675402'


@pytest.fixture
def exist_credit_card():
    return '1099-1111-2314-1234'


def test_update_customer_positive(update_customer_facade: CustomerFacade, update_customer_valid):
    try:
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
    except Exception as exc:
        assert False, f'exception raised: {str(exc)}'
    # SUCCEDDED
    try:
        customer = update_customer_facade.get_customer_by_id(update_customer_valid.id)
        if customer is None:
            assert False, f'customer updated but returned None customer'
        if customer != update_customer_valid:
            assert False, f'updated custoer and retuerned customer are different'
        assert True
    except Exception as exc:
        assert False, f'exception raised in the test code {str(exc)}'


def test_update_customer_neg_invalid_token(update_customer_facade: CustomerFacade, update_customer_valid):
    try:
        # INVALID TOKEN CUSTOMER ID = 2
        update_customer_valid.id = 2
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, InvalidTokenException):
            assert False, f'test falied: not InvalidTokenException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# update ==> cusotmer not exists
def test_update_customer_neg_not_exists(update_customer_facade: CustomerFacade, update_customer_not_exists):
    try:
        update_customer_facade.update_customer(update_customer_not_exists.id, update_customer_not_exists)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.CUSTOMER:
            assert False, f'test falied: not CUSTOMER NotFoundException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# update ==> empty
def test_update_customer_neg_firstname_empty(update_customer_facade: CustomerFacade, update_customer_valid):
    try:
        update_customer_valid.first_name = ''
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.CUSTOMER_FIRST_NAME:
            assert False, f'test falied: not EMPTY/CUSTOMER_FIRST_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_update_customer_neg_lastname_empty(update_customer_facade, update_customer_valid):
    try:
        update_customer_valid.last_name = ''
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.CUSTOMER_LAST_NAME:
            assert False, f'test falied: not EMPTY/CUSTOMER_LAST_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_update_customer_neg_address_empty(update_customer_facade, update_customer_valid):
    try:
        update_customer_valid.address = ''
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.CUSTOMER_ADDRESS_NAME:
            assert False, f'test falied: not EMPTY/CUSTOMER_ADDRESS_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_update_customer_neg_phone_empty(update_customer_facade, update_customer_valid):
    try:
        update_customer_valid.phone_number = ''
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.CUSTOMER_PHONE_NAME:
            assert False, f'test falied: not EMPTY/CUSTOMER_PHONE_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_update_customer_neg_creditcard_empty(update_customer_facade, update_customer_valid):
    try:
        update_customer_valid.credit_card_number = ''
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.CUSTOMER_CREDIT_CARD:
            assert False, f'test falied: not EMPTY/CUSTOMER_CREDIT_CARD NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# update customer==> invalid input
def test_update_customer_neg_firstname_too_long(update_customer_facade, update_customer_valid):
    update_customer_valid.first_name = ('D' * 51)
    try:
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.TOO_LONG or inner.field_name != Field.CUSTOMER_FIRST_NAME:
            assert False, f'test falied: not TOO_LONG/CUSTOMER_CREDIT_CARD NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_update_customer_neg_lastname_too_long(update_customer_facade, update_customer_valid):
    update_customer_valid.last_name = ('D' * 51)
    try:
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.TOO_LONG or inner.field_name != Field.CUSTOMER_LAST_NAME:
            assert False, f'test falied: not TOO_LONG/CUSTOMER_LAST_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_update_customer_neg_adrres_too_long(update_customer_facade, update_customer_valid):
    update_customer_valid.address = ('D' * 201)
    try:
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.TOO_LONG or inner.field_name != Field.CUSTOMER_ADDRESS_NAME:
            assert False, f'test falied: not TOO_LONG/CUSTOMER_ADDRESS_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_update_customer_neg_phone_too_long(update_customer_facade, update_customer_valid):
    update_customer_valid.phone_number = ('1' * 21)
    try:
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.TOO_LONG or inner.field_name != Field.CUSTOMER_PHONE_NAME:
            assert False, f'test falied: not TOO_LONG/CUSTOMER_PHONE_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_update_customer_credit_card_number_too_long(update_customer_facade, update_customer_valid):
    update_customer_valid.credit_card_number = ('1' * 25)
    try:
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.TOO_LONG or inner.field_name != Field.CUSTOMER_CREDIT_CARD:
            assert False, f'test falied: not TOO_LONG/CUSTOMER_CREDIT_CARD NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_update_customer_neg_user_id_not_exists(update_customer_facade, update_customer_valid):
    update_customer_valid.user_id = 0
    try:
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.USER:
            assert False, f'test falied: not USER NotFoundException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# phone unique constraint violation
def test_update_customer_neg_phone_exists(update_customer_facade, update_customer_valid, exist_phone):
    update_customer_valid.phone_number = '0502224730'
    try:
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotUniqueException):
            assert False, f'test falied: not NotUniqueException exception: {str(inner)}'
        if inner.field_name != Field.CUSTOMER_PHONE_NAME:
            assert False, f'test falied: not CUSTOMER_PHONE_NAME NotUniqueException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_update_customer_neg_creditcard_exists(update_customer_facade, update_customer_valid, exist_credit_card):
    update_customer_valid.credit_card_number = '1070-1322-2828-1524'
    try:
        update_customer_facade.update_customer(update_customer_valid.id, update_customer_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotUniqueException):
            assert False, f'test falied: not NotUniqueException exception: {str(inner)}'
        if inner.field_name != Field.CUSTOMER_CREDIT_CARD:
            assert False, f'test falied: not CUSTOMER_CREDIT_CARD NotUniqueException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# ******************************
# ADD TICKET

@pytest.fixture
def new_valid_ticket():
    return Ticket(flight_id=8, customer_id=2)


@pytest.fixture
def cross_flight_ticket():
    return Ticket(flight_id=9, customer_id=2)


@pytest.fixture
def not_found_flight_id():
    return 999


@pytest.fixture
def not_found_cust_id():
    return 999


@pytest.fixture
def departured_flight_id():
    return 1


@pytest.fixture
def outoftickets_flight_id():
    return 3


@pytest.fixture
def user_overlapped_flight_id():
    return 3


def test_add_ticket_positive(add_ticket_facade: CustomerFacade, new_valid_ticket: Ticket):
    remaining_tickets_before = None
    try:
        flight_before = add_ticket_facade.get_flight_by_id(new_valid_ticket.flight_id)
        remaining_tickets_before = flight_before.remaining_tickets
        add_ticket_facade.add_ticket(new_valid_ticket)
    except Exception as exc:
        assert False, f'exception is raised, {str(exc)}'
    # SUCCEDDED:
    try:
        ticket = add_ticket_facade.get_ticket_by_id(new_valid_ticket.id)
        if ticket is None:
            assert False, f'inserted but returned ticket id none!'
        if ticket != new_valid_ticket:
            assert False, f'inserted, but tickets are different!'
        flight_after = add_ticket_facade.get_flight_by_id(new_valid_ticket.flight_id)
        is_decrement_ticket = flight_after.remaining_tickets == (remaining_tickets_before - 1)
        if not is_decrement_ticket:
            assert False, f'inserted but returned ticket balance not minus 1!'
        assert True
    except Exception as exc:
        assert False, f'exception raised in the test code {str(exc)}'


def test_add_ticket_negative_invalid_token(add_ticket_facade: CustomerFacade, new_valid_ticket: Ticket):
    try:
        # INVALID TOKEN CUSTOMER ID = 1
        new_valid_ticket.customer_id = 1
        add_ticket_facade.add_ticket(new_valid_ticket)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, InvalidTokenException):
            assert False, f'test falied: not NotValidOrderException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_ticket_negative_cross_fight_exists(add_ticket_facade: CustomerFacade, cross_flight_ticket: Ticket):
    try:
        add_ticket_facade.add_ticket(cross_flight_ticket)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotValidOrderException):
            assert False, f'test falied: not NotValidOrderException exception: {str(inner)}'
        if inner.cause != Reason.CROSS_FLIGHT:
            assert False, f'test falied: not CROSS_FLIGHT NotValidOrderException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_ticket_negative_flight_not_exists(add_ticket_facade: CustomerFacade, new_valid_ticket: Ticket,
                                               not_found_flight_id):
    new_valid_ticket.flight_id = not_found_flight_id
    try:
        add_ticket_facade.add_ticket(new_valid_ticket)
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


def test_add_ticket_negative_customer_not_exists(add_ticket_facade: CustomerFacade, new_valid_ticket: Ticket, not_found_cust_id):
    new_valid_ticket.customer_id = not_found_cust_id
    try:
        add_ticket_facade.add_ticket(new_valid_ticket)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.CUSTOMER:
            assert False, f'test falied: not CUSTOMER NotFoundException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_ticket_neg_flight_allready_departured(add_ticket_facade: CustomerFacade, new_valid_ticket: Ticket,
                                                   departured_flight_id):
    new_valid_ticket.flight_id = departured_flight_id
    try:
        add_ticket_facade.add_ticket(new_valid_ticket)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotValidOrderException):
            assert False, f'test falied: not NotValidOrderException exception: {str(inner)}'
        if inner.cause != Reason.FLIGHT_ALLREADY_DEPARTURED:
            assert False, f'test falied: not FLIGHT_ALLREADY_DEPARTURED NotValidOrderException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_ticket_neg_flight_outoftickets(add_ticket_facade: CustomerFacade, new_valid_ticket: Ticket, outoftickets_flight_id):
    new_valid_ticket.flight_id = outoftickets_flight_id
    try:
        add_ticket_facade.add_ticket(new_valid_ticket)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotValidOrderException):
            assert False, f'test falied: not NotValidOrderException exception: {str(inner)}'
        if inner.cause != Reason.FLIGHT_SOLD_OUT:
            assert False, f'test falied: not FLIGHT_SOLD_OUT NotValidOrderException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# **********************************************************
# REMOVE TICKET
@pytest.fixture
def remove_ticket_user():
    # CUSTOMER ID = 2
    return {'username': 'Stav1221', 'password': '8765432X'}


@pytest.fixture
def remove_ticket_facade(facade: AnonymousFacade, remove_ticket_user):
    customer_facade = facade.login(remove_ticket_user['username'], remove_ticket_user['password'])
    return customer_facade


@pytest.fixture
def valid_ticket_id_to_remove():
    return 1


@pytest.fixture
def not_exists_ticket_id():
    return 999


@pytest.fixture
def ticket_with_flight_departured():
    return 4


@pytest.fixture
def valid_ticket_customer_id():
    return 3


def test_remove_ticket_positive(remove_ticket_facade: CustomerFacade, valid_ticket_id_to_remove):
    flight_before = None
    remaining_tickets_before = None
    try:
        ticket = remove_ticket_facade.get_ticket_by_id(valid_ticket_id_to_remove)
        flight_before = remove_ticket_facade.get_flight_by_id(ticket.flight_id)
        remaining_tickets_before = flight_before.remaining_tickets
        remove_ticket_facade.remove_ticket(valid_ticket_id_to_remove)
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'
    try:
        ticket = remove_ticket_facade.get_ticket_by_id(valid_ticket_id_to_remove)
        if ticket is not None:
            assert False, f'ticket {valid_ticket_id_to_remove} deleted but still exists!'
        flight_after = remove_ticket_facade.get_flight_by_id(flight_before.id)
        is_increment_ticket = flight_after.remaining_tickets == (remaining_tickets_before + 1)
        if not is_increment_ticket:
            assert False, f'inserted but returned ticket balance not minus 1!'
        assert True
    except Exception as exc:
        assert False, f'exception raised in the test code {str(exc)}'


def test_reomve_ticket_neg_invalid_token(remove_ticket_facade: CustomerFacade):
    try:
        # INVALID TOKEN CUSTOMER TICKET ID = 1
        invalid_ticket_id_to_remove = 3
        remove_ticket_facade.remove_ticket(invalid_ticket_id_to_remove)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, InvalidTokenException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_reomve_ticket_neg_ticket_not_exists(remove_ticket_facade: CustomerFacade, not_exists_ticket_id):
    try:
        remove_ticket_facade.remove_ticket(not_exists_ticket_id)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.TICKET:
            assert False, f'test falied: not TICKET NotFoundException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_reomve_ticket_flight_allready_departured(remove_ticket_facade: CustomerFacade, ticket_with_flight_departured):
    try:
        remove_ticket_facade.remove_ticket(ticket_with_flight_departured)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotValidOrderException):
            assert False, f'test falied: not NotValidOrderException exception: {str(inner)}'
        if inner.cause != Reason.FLIGHT_ALLREADY_DEPARTURED:
            assert False, f'test falied: not FLIGHT_ALLREADY_DEPARTURED NotValidOrderException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# **********************
# GET MY TICKETS
@pytest.fixture(scope='session', autouse=True)
def get_my_ticket_user():
    # CUSTOMER ID = 3
    return {'username': 'Itay1221', 'password': '13243546'}


@pytest.fixture(scope='session', autouse=True)
def get_my_ticket_facade(facade: AnonymousFacade, get_my_ticket_user):
    customer_facade = facade.login(get_my_ticket_user['username'], get_my_ticket_user['password'])
    return customer_facade


def test_get_my_tickets_positive(get_my_ticket_facade: CustomerFacade, valid_ticket_customer_id):
    try:
        customer_tickets = get_my_ticket_facade.get_my_tickets(valid_ticket_customer_id)
        if len(customer_tickets) > 0:
            not_customer_ticket = next((x for x in customer_tickets if x.customer_id != valid_ticket_customer_id), None)
            if not_customer_ticket is not None:
                assert False, f'ticket {not_customer_ticket.id} not belong to customer{valid_ticket_customer_id}'
        assert True
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'


def test_get_my_fligths_positive(get_my_ticket_facade: CustomerFacade, valid_ticket_customer_id):
    try:
        customer_flights = get_my_ticket_facade.get_flights_by_customer(valid_ticket_customer_id)
        assert True
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'


def test_get_tickets_by_customer_neg_customer_not_exist(get_my_ticket_facade: CustomerFacade, not_found_cust_id):
    try:
        tickets = get_my_ticket_facade.get_my_tickets(not_found_cust_id)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.CUSTOMER:
            assert False, f'test falied: not CUSTOMER NotFoundException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_get_tickets_by_customer_neg_invalid_token(get_my_ticket_facade: CustomerFacade):
    try:
        # INVALID TOKET CUSTOMER ID = 2
        invalid_customer_id = 2
        tickets = get_my_ticket_facade.get_my_tickets(invalid_customer_id)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, InvalidTokenException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'