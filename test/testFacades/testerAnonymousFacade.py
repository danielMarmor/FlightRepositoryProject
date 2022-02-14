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
# LOGIN

@pytest.fixture
def exists_username():
    return 'Daniel1221'


# login ===> exists password in system
@pytest.fixture
def exists_password():
    return '12345678'


# login ===> not exists username in system
@pytest.fixture
def not_exist_username():
    return 'XXXXXXXX'


@pytest.fixture
def empty_user_name():
    return ''

# login/create new user ===> empty password
@pytest.fixture
def empty_password():
    return ''


# login ===> not exists password in system
@pytest.fixture
def not_exist_password():
    return 'XXXXXXXX'


# customer
@pytest.fixture
def exists_customer_user():
    return {'username': 'Daniel1221', 'password': '12345678'}


# admin
@pytest.fixture
def exists_admin_user():
    return {'username': 'danielma', 'password': 'danielma440'}


# airline
@pytest.fixture
def exists_airline_user():
    return {'username': 'british123', 'password': '016677098$3'}


# login/create new user ===> empty password
def test_user_login_positive_get_customer(facade, exists_customer_user):
    try:
        customer_facade = facade.login(exists_customer_user['username'], exists_customer_user['password'])
        if customer_facade is None:
            assert False, f'returned customer_facade user = None'
        if not isinstance(customer_facade, CustomerFacade):
            assert False, f'returned user not customer_facade type'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_user_login_positive_get_airline(facade, exists_airline_user):
    try:
        airline_facade = facade.login(exists_airline_user['username'], exists_airline_user['password'])
        if airline_facade is None:
            assert False, f'returned airline_facade user = None'
        if not isinstance(airline_facade, AirlineFacade):
            assert False, f'returned user not AirlineFacade type'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_user_login_positive_get_admin(facade, exists_admin_user):
    try:
        admin_facade = facade.login(exists_admin_user['username'], exists_admin_user['password'])
        if admin_facade is None:
            assert False, f'returned admin_facade user = None'
        if not isinstance(admin_facade, AdministratorFacade):
            assert False, f'returned user not AdministratorFacade type'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# when username is empty
def test_user_login_empty_username(facade, empty_user_name, exists_password):
    try:
        result_facade = facade.login(empty_user_name, exists_password)
        assert False, f'test falied: user name is empty'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception :{str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.USER_NAME:
            assert False, f'test falied: not EMPTY/USER_NAME exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# when username is empty
def test_user_login_empty_pasword(facade, exists_username, empty_password):
    try:
        result_facade = facade.login(exists_username, empty_password)
        assert False, f'test falied: user name is empty'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception :{str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.USER_PASSWORD:
            assert False, f'test falied: not EMPTY/USER_PASSWORD exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# when username not exists
def test_user_login_user_invalid_username(facade, not_exist_username, exists_password):
    try:
        result_facade = facade.login(not_exist_username, exists_password)
        assert False, f'user not valid by username {not_exist_username} but login'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotValidLoginException):
            assert False, f'test falied: not NotValidLoginException exception :{str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# when password not exists
def test_user_login_user_invalid_password(facade, exists_username, not_exist_password):
    try:
        result_facade = facade.login(exists_username, not_exist_password)
        assert False, f'user not valid by password {not_exist_password} but login'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotValidLoginException):
            assert False, f'test falied: not NotValidLoginException exception :{str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# ******************************************************************
# ADD CUSTOMER
@pytest.fixture
def new_customer_valid():
    # SONY SOCK
    return Customer(first_name='   Sony',
                    last_name='    Smith',
                    address='Rondeo Street 20 Ayova',
                    phone_number='054055002',
                    credit_card_number='1040-3004-1322-7484',
                    user_id=4)


@pytest.fixture
def new_user_valid():
    return User(username='sony0122', password='1234509_X', email='sonysony@gmail.com', user_role=UserRoles.CUSTOMER)


@pytest.fixture
def new_user_not_valid_user_name():
    return User(username='', password='1234509_X', email='sonysony@gmail.com', user_role=USER_ROLE_ADMIN)


@pytest.fixture
def new_user_not_valid_user_password():
    return User(username='sony0122', password='XXX', email='sonysony@gmail.com', user_role=USER_ROLE_ADMIN)


@pytest.fixture
def new_user_not_valid_user_email():
    return User(username='sony0122', password='12345678', email='F'*60,
                user_role=USER_ROLE_ADMIN)


@pytest.fixture
def new_user_not_valid_user_role():
    return User(username='sony0122', password='12345678', email='sonysony@gmail.com', user_role=0)


@pytest.fixture
def new_user_not_unique_user():
    return User(username='Daniel1221', password='12345678', email='danielmaraor2@unique.com', user_role=USER_ROLE_ADMIN)


@pytest.fixture
def new_user_not_unique_email():
    return User(username='daniel3223', password='12345678', email='danielmarmor2@gmail.com', user_role=USER_ROLE_ADMIN)


@pytest.fixture
def exist_phone():
    return '0543675402'


@pytest.fixture
def exist_credit_card():
    return '1099-1111-2314-1234'


@pytest.fixture
def exists_customer_user():
    return {'username': 'Daniel1221', 'password': '12345678'}


def test_add_customer_positive(facade: AnonymousFacade, new_customer_valid, new_user_valid):
    try:
        facade.add_customer(new_customer_valid, new_user_valid)
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'
    try:
        customer = facade.get_customer_by_id(new_customer_valid.id)
        if customer is None:
            assert False, f'customer inserted id:{new_customer_valid.id} but no return customer'
        if customer != new_customer_valid:
            assert False
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised but only in the test process: {str(exc)}'


def test_add_customer_negative_not_valid_username(facade: AnonymousFacade, new_customer_valid,
                                                  new_user_not_valid_user_name):
    try:
        facade.add_customer(new_customer_valid, new_user_not_valid_user_name)
        assert False, f'test failed: should not insert not-valid username:{new_user_not_valid_user_name.username}'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotValidLoginException exception :{str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_customer_negative_not_valid_password(facade, new_customer_valid, new_user_not_valid_user_password):
    try:
        facade.add_customer(new_customer_valid, new_user_not_valid_user_password)
        assert False, f'test failed: should not insert not-valid password:{new_user_not_valid_user_password.password}'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_customer_negative_not_valid_email(facade, new_customer_valid, new_user_not_valid_user_email):
    try:
        facade.add_customer(new_customer_valid, new_user_not_valid_user_email)
        assert False, f'test failed: should not insert not-valid email:{new_user_not_valid_user_email.email}'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_customer_negative_not_unique_username(facade, new_customer_valid, new_user_not_unique_user):
    try:
        facade.add_customer(new_customer_valid, new_user_not_unique_user)
        assert False, f'test failed: should not insert not-unique username:{new_user_not_unique_user.username}'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotUniqueException):
            assert False, f'test falied: not NotUniqueException exception: {str(inner)}'
        if inner.action != Actions.CREATE_NEW_USER or inner.field_name != Field.USER_NAME:
            assert False, f'test falied: not CREATE_NEW_USER/USER_PASSWORD exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_customer_negative_not_unique_email(facade, new_customer_valid,  new_user_not_unique_email):
    try:
        facade.add_customer(new_customer_valid, new_user_not_unique_email)
        assert False, f'test failed: should not insert not-unique email:{new_user_not_unique_email.email}'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotUniqueException):
            assert False, f'test falied: not NotUniqueException exception: {str(inner)}'
        if inner.action != Actions.CREATE_NEW_USER or inner.field_name != Field.USER_EMAIL:
            assert False, f'test falied: not CREATE_NEW_USER/USER_EMAIL exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# add customer- empty values
def test_add_customer_neg_firstname_empty(facade, new_customer_valid, new_user_valid):
    try:
        new_customer_valid.first_name = ''
        facade.add_customer(new_customer_valid, new_user_valid)
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


def test_add_customer_neg_lastname_empty(facade, new_customer_valid, new_user_valid):
    try:
        new_customer_valid.last_name = ''
        facade.add_customer(new_customer_valid, new_user_valid)
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


def test_add_customer_neg_address_empty(facade, new_customer_valid, new_user_valid):
    try:
        new_customer_valid.address = ''
        facade.add_customer(new_customer_valid, new_user_valid)
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


def test_add_customer_neg_phone_empty(facade, new_customer_valid, new_user_valid):
    try:
        new_customer_valid.phone_number = ''
        facade.add_customer(new_customer_valid, new_user_valid)
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


def test_add_customer_neg_creditcard_empty(facade: CustomerFacade, new_customer_valid, new_user_valid):
    try:
        new_customer_valid.credit_card_number = ''
        facade.add_customer(new_customer_valid, new_user_valid)
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


# no valid customer values
# firstname ==> too long
def test_add_customer_neg_firstname_too_long(facade, new_customer_valid, new_user_valid):
    new_customer_valid.first_name = ('D' * 51)
    try:
        facade.add_customer(new_customer_valid, new_user_valid)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.TOO_LONG or inner.field_name != Field.CUSTOMER_FIRST_NAME:
            assert False, f'test falied: not TOO_LONG/CUSTOMER_FIRST_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_customer_neg_lastname_too_long(facade, new_customer_valid, new_user_valid):
    new_customer_valid.last_name = ('D' * 51)
    try:
        facade.add_customer(new_customer_valid, new_user_valid)
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


def test_add_customer_neg_adrres_too_long(facade, new_customer_valid, new_user_valid):
    new_customer_valid.address = ('D' * 201)
    try:
        facade.add_customer(new_customer_valid, new_user_valid)
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


def test_add_customer_neg_phone_too_long(facade, new_customer_valid, new_user_valid):
    new_customer_valid.phone_number = ('1' * 21)
    try:
        facade.add_customer(new_customer_valid, new_user_valid)
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


def test_add_customer_credit_card_number_too_long(facade, new_customer_valid, new_user_valid):
    new_customer_valid.credit_card_number = ('1' * 25)
    try:
        facade.add_customer(new_customer_valid, new_user_valid)
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


def test_add_customer_neg_phone_exists(facade, new_customer_valid, exist_phone, new_user_valid):
    new_customer_valid.phone_number = exist_phone
    try:
        facade.add_customer(new_customer_valid, new_user_valid)
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


# creditcard unique constraint violation
def test_add_customer_neg_creditcard_exists(facade, new_customer_valid, exist_credit_card, new_user_valid):
    new_customer_valid.credit_card_number = exist_credit_card
    try:
        facade.add_customer(new_customer_valid, new_user_valid)
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




