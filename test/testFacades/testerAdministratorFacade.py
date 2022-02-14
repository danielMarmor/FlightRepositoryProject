import pytest
from common.constants.settings import USER_ROLE_ADMIN
from dataAccess.FlightRepository import FilghtRepository
from business.facade.anonymousFacade import *
from business.facade.administratorFacade import AdministratorFacade
from business.services.loginService import *
from business.services.testService import TestService
from common.entities.User import User
from common.entities.Flight import Flight
from common.entities.AirlineCompany import AirlineCompany
from common.exceptions.notUniqueException import NotUniqueException
from business.services.genericService import GenericService
from common.entities.db_config import local_session, create_all_entities, connection_string
from common.entities.db_conifg_procedured import load_db_scripts
from common.exceptions.notFoundException import NotFoundException
from common.entities.Customer import Customer
from common.entities.Administrator import Administrator
from common.exceptions.invalidTokenException import InvalidTokenException


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
# GET ALL CUSTOMERS
@pytest.fixture
def exists_administrator():
    return {'username': 'danielma', 'password': 'danielma440'}


@pytest.fixture
def get_my_customers_facade(facade: AnonymousFacade, exists_administrator):
    admin_facade = facade.login(exists_administrator['username'], exists_administrator['password'])
    return admin_facade


def test_get_all_customers_positive(get_my_customers_facade: AdministratorFacade):
    try:
        customers = get_my_customers_facade.get_all_customers()
        assert True
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'


# **************************************************************

@pytest.fixture
def new_vailid_airline():
    return AirlineCompany(name='Lufthanza', country_id=3, user_id=6)


@pytest.fixture
def new_airline_user():
    return User(username='luft123', password='015180098$3', email='lufthanza@gmail.com',
                user_role=2)


# ADD AIRLINE
@pytest.fixture
def add_airline_facade(facade: AnonymousFacade, exists_administrator):
    admin_facade = facade.login(exists_administrator['username'], exists_administrator['password'])
    return admin_facade


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
def not_unique_airline_name():
    return 'British Airways'


# ADD AIRLINE
def test_add_airline_positive(add_airline_facade: AdministratorFacade, new_vailid_airline, new_airline_user):
    try:
        add_airline_facade.add_airline(new_vailid_airline, new_airline_user)
    except Exception as exc:
        print(f'exception is raised: {str(exc)}')
        assert False, f'exception is raised: {str(exc)}'
    # SUCCEDED :
    try:
        airline = add_airline_facade.get_airline_by_id(new_vailid_airline.id)
        if airline is None:
            assert False, 'inserted but returns airline None'
        if airline != new_vailid_airline:
            assert False, 'inserted but return airline is not identical'
        assert True
    except Exception as exc:
        print(f'exception is raised (but only on test code): {str(exc)}')
        assert False, f'exception is raised (but only on test code): {str(exc)}'


def test_add_airline_neg_not_valid_username(add_airline_facade: AdministratorFacade, new_vailid_airline,
                                            new_user_not_valid_user_name):
    try:
        add_airline_facade.add_airline(new_vailid_airline, new_user_not_valid_user_name)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_airline_neg_not_valid_password(add_airline_facade: AdministratorFacade, new_vailid_airline,
                                            new_user_not_valid_user_password):
    try:
        add_airline_facade.add_airline(new_vailid_airline, new_user_not_valid_user_password)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_airline_neg_not_valid_email(add_airline_facade: AdministratorFacade, new_vailid_airline,
                                         new_user_not_valid_user_email):
    try:
        add_airline_facade.add_airline(new_vailid_airline, new_user_not_valid_user_email)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_airline_neg_empty_name(add_airline_facade: AdministratorFacade, new_vailid_airline, new_airline_user):
    new_vailid_airline.name = ''
    try:
        add_airline_facade.add_airline(new_vailid_airline, new_airline_user)
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
def test_add_airline_neg_empty_country_id(add_airline_facade: AdministratorFacade, new_vailid_airline, new_airline_user):
    new_vailid_airline.country_id = None
    try:
        add_airline_facade.add_airline(new_vailid_airline, new_airline_user)
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
# def test_add_airline_neg_empty_user_id(add_airline_facade: AdministratorFacade, new_vailid_airline, new_airline_user):
#     new_vailid_airline.user_id = None
#     try:
#         add_airline_facade.add_airline(new_vailid_airline, new_airline_user)
#         assert False
#     except FlightSystemException as exc:
#         inner = GenericService.get_root_exception(exc)
#         if not isinstance(inner, NotVaildInputException):
#             assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
#         if inner.cause != Reason.EMPTY or inner.field_name != Field.AIRLINE_USER_ID:
#             assert False, f'test falied: not EMPTY/AIRLINE_USER_ID NotVaildInputException'
#         assert True
#     except Exception as exc:
#         assert False, f'test failed because of an exception : {str(exc)}'


# invalid name
def test_add_airline_neg_name_too_long(add_airline_facade: AdministratorFacade, new_vailid_airline, new_airline_user):
    new_vailid_airline.name = 'A' * (AirlineCompany.MAX_NAME + 1)
    try:
        add_airline_facade.add_airline(new_vailid_airline, new_airline_user)
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
def test_add_airline_neg_not_exists_country_id(add_airline_facade: AdministratorFacade, new_vailid_airline,
                                               new_airline_user):
    new_vailid_airline.country_id = -999
    try:
        add_airline_facade.add_airline(new_vailid_airline, new_airline_user)
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


# # not exists_user_id
# def test_add_airline_neg_not_exists_user_id(add_airline_facade: AdministratorFacade, new_vailid_airline,
#                                             new_airline_user):
#     new_vailid_airline.user_id = -999
#     try:
#         add_airline_facade.add_airline(new_vailid_airline, new_airline_user)
#         assert False
#     except FlightSystemException as exc:
#         inner = GenericService.get_root_exception(exc)
#         if not isinstance(inner, NotFoundException):
#             assert False, f'test falied: not NotFoundException exception: {str(inner)}'
#         if inner.entity != Entity.USER:
#             assert False, f'test falied: not USER NotFoundException'
#         assert True
#     except Exception as exc:
#         assert False, f'test failed because of an exception : {str(exc)}'


# allready exists by name
def test_add_airline_neg_not_unique_name(add_airline_facade: AdministratorFacade, new_vailid_airline,
                                         new_airline_user, not_unique_airline_name):
    new_vailid_airline.name = not_unique_airline_name
    try:
        add_airline_facade.add_airline(new_vailid_airline, new_airline_user)
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


# **************************************************************8
# ADD CUSTOMER
@pytest.fixture
def add_customer_facade(facade: AnonymousFacade, exists_administrator):
    admin_facade = facade.login(exists_administrator['username'], exists_administrator['password'])
    return admin_facade


@pytest.fixture
def new_customer_valid():
    # SONY SOCK
    return Customer(first_name='   greenwood',
                    last_name='    baze',
                    address='Rondeo Street 20 Ayova',
                    phone_number='054055002',
                    credit_card_number='1040-3004-1322-7484')


@pytest.fixture
def new_customer_user():
    return User(username='greenwood', password='q5444y788', email='greenwood@gmail.com',
                user_role=1)


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


def test_add_customer_positive(add_customer_facade :AdministratorFacade, new_customer_valid, new_customer_user):
    try:
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'
    try:
        customer = add_customer_facade.get_customer_by_id(new_customer_valid.id)
        if customer is None:
            assert False, f'customer inserted id:{new_customer_valid.id} but no return customer'
        if customer != new_customer_valid:
            assert False
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised but only in the test process: {str(exc)}'


def test_add_customer_negative_not_valid_username(add_customer_facade: AdministratorFacade, new_customer_valid,
                                                  new_user_not_valid_user_name):
    try:
        add_customer_facade.add_customer(new_customer_valid, new_user_not_valid_user_name)
        assert False, f'test failed: should not insert not-valid username:{new_user_not_valid_user_name.username}'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotValidLoginException exception :{str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_customer_negative_not_valid_password(add_customer_facade: AdministratorFacade, new_customer_valid,
                                                  new_user_not_valid_user_password):
    try:
        add_customer_facade.add_customer(new_customer_valid, new_user_not_valid_user_password)
        assert False, f'test failed: should not insert not-valid password:{new_user_not_valid_user_password.password}'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_customer_negative_not_valid_email(add_customer_facade: AdministratorFacade, new_customer_valid,
                                               new_user_not_valid_user_email):
    try:
        add_customer_facade.add_customer(new_customer_valid, new_user_not_valid_user_email)
        assert False, f'test failed: should not insert not-valid email:{new_user_not_valid_user_email.email}'
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_customer_negative_not_unique_username(add_customer_facade: AdministratorFacade, new_customer_valid,
                                                   new_user_not_unique_user):
    try:
        add_customer_facade.add_customer(new_customer_valid, new_user_not_unique_user)
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


def test_add_customer_negative_not_unique_email(add_customer_facade: AdministratorFacade, new_customer_valid,
                                                new_user_not_unique_email):
    try:
        add_customer_facade.add_customer(new_customer_valid, new_user_not_unique_email)
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
def test_add_customer_neg_firstname_empty(add_customer_facade :AdministratorFacade, new_customer_valid,
                                          new_customer_user):
    try:
        new_customer_valid.first_name = ''
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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


def test_add_customer_neg_lastname_empty(add_customer_facade: AdministratorFacade, new_customer_valid,
                                         new_customer_user):
    try:
        new_customer_valid.last_name = ''
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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


def test_add_customer_neg_address_empty(add_customer_facade: AdministratorFacade, new_customer_valid,
                                        new_customer_user):
    try:
        new_customer_valid.address = ''
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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


def test_add_customer_neg_phone_empty(add_customer_facade :AdministratorFacade, new_customer_valid,
                                      new_customer_user):
    try:
        new_customer_valid.phone_number = ''
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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


def test_add_customer_neg_creditcard_empty(add_customer_facade: AdministratorFacade, new_customer_valid,
                                           new_customer_user):
    try:
        new_customer_valid.credit_card_number = ''
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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
def test_add_customer_neg_firstname_too_long(add_customer_facade: AdministratorFacade, new_customer_valid,
                                             new_customer_user):
    new_customer_valid.first_name = ('D' * 51)
    try:
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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


def test_add_customer_neg_lastname_too_long(add_customer_facade: AdministratorFacade, new_customer_valid,
                                            new_customer_user):
    new_customer_valid.last_name = ('D' * 51)
    try:
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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


def test_add_customer_neg_adrres_too_long(add_customer_facade: AdministratorFacade, new_customer_valid,
                                          new_customer_user):
    new_customer_valid.address = ('D' * 201)
    try:
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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


def test_add_customer_neg_phone_too_long(add_customer_facade: AdministratorFacade, new_customer_valid,
                                         new_customer_user):
    new_customer_valid.phone_number = ('1' * 21)
    try:
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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


def test_add_customer_credit_card_number_too_long(add_customer_facade: AdministratorFacade, new_customer_valid,
                                                  new_customer_user):
    new_customer_valid.credit_card_number = ('1' * 25)
    try:
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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


def test_add_customer_neg_phone_exists(add_customer_facade: AdministratorFacade, new_customer_valid, exist_phone,
                                       new_customer_user):
    new_customer_valid.phone_number = exist_phone
    try:
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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
def test_add_customer_neg_creditcard_exists(add_customer_facade: AdministratorFacade, new_customer_valid,
                                            exist_credit_card, new_customer_user):
    new_customer_valid.credit_card_number = exist_credit_card
    try:
        add_customer_facade.add_customer(new_customer_valid, new_customer_user)
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

# ************************************************
# REMOVE AIRLINE
@pytest.fixture
def remove_airline_facade(facade: AnonymousFacade, exists_administrator):
    admin_facade = facade.login(exists_administrator['username'], exists_administrator['password'])
    return admin_facade


@pytest.fixture
def airline_id_to_remove():
    return 2  # british airways


def test_remove_airline_positive(remove_airline_facade: AdministratorFacade, airline_id_to_remove):
    try:
        remove_airline_facade.remove_airline(airline_id_to_remove)
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'
    try:
        airline = remove_airline_facade.get_airline_by_id(airline_id_to_remove)
        if airline is not None:
            assert False, f'airline removed but airline returns'
        assert True
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException'
        if inner.entity != Entity.AIRLINE_COMPANY:
            assert False, f'test falied: not AIRLINE_COMPANY NotFoundException'
        assert True
    except Exception as exc:
        assert False, f'exception raised (only in test code), {str(exc)}'


# negative- airline not found
def test_remove_airline_neg_airline_not_found(remove_airline_facade: AdministratorFacade):
    try:
        airline_id_not_found = -999
        remove_airline_facade.remove_airline(airline_id_not_found)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.AIRLINE_COMPANY:
            assert False, f'test falied: not AIRLINE_COMPANY NotFoundException'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# ********************************************8
# REMOVE CUSTOMER
@pytest.fixture
def remove_customer_facade(facade: AnonymousFacade, exists_administrator):
    admin_facade = facade.login(exists_administrator['username'], exists_administrator['password'])
    return admin_facade


@pytest.fixture
def customer_id_to_remove():
    return 2


def test_remove_customer_positive(remove_customer_facade: AdministratorFacade, customer_id_to_remove):
    try:
        remove_customer_facade.remove_customer(customer_id_to_remove)
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'
    try:
        customer = remove_customer_facade.get_customer_by_id(customer_id_to_remove)
        if customer is not None:
            assert False, f'customer removed but customer returns'
        assert True
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException'
        if inner.entity != Entity.CUSTOMER:
            assert False, f'test falied: not CUSTOMER NotFoundException'
        assert True
    except Exception as exc:
        assert False, f'exception raised (only in test code), {str(exc)}'


def test_remove_customer_neg_cust_not_found(remove_customer_facade: AdministratorFacade):
    try:
        customer_id_not_found = -999
        remove_customer_facade.remove_customer(customer_id_not_found)
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


# *****************************************
# ADD ADMINISTRATOR
@pytest.fixture
def add_aministrator_facade(facade: AnonymousFacade, exists_administrator):
    admin_facade = facade.login(exists_administrator['username'], exists_administrator['password'])
    return admin_facade


@pytest.fixture
def new_admin_valid():
    return Administrator(first_name='Simon',
                         last_name='Levayev')


@pytest.fixture
def new_administrator_user():
    return User(username='Simon99', password='45444MMV', email='simonlevayev@gmail.com',
                user_role=3)


def test_add_administrator_positive(add_aministrator_facade: AdministratorFacade, new_admin_valid, new_administrator_user):
    try:
        add_aministrator_facade.add_administrator(new_admin_valid, new_administrator_user)
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'
    try:
        administrator = add_aministrator_facade.get_administrator_by_id(new_admin_valid.id)
        if administrator is None:
            assert False, f'administrator inserted id:{new_admin_valid.id} but no return administrator'
        if administrator != new_admin_valid:
            assert False
        assert True
    except Exception as exc:
        assert False, f'Exception is Raised but only in the test process: {str(exc)}'


def test_add_administrator_neg_username_not_valid(add_aministrator_facade: AdministratorFacade,
                                                  new_admin_valid, new_user_not_valid_user_name):
    try:
        add_aministrator_facade.add_administrator(new_admin_valid, new_user_not_valid_user_name)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_administrator_neg_password_not_valid(add_aministrator_facade: AdministratorFacade,
                                                  new_admin_valid, new_user_not_valid_user_password):
    try:
        add_aministrator_facade.add_administrator(new_admin_valid, new_user_not_valid_user_password)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_administrator_neg_email_not_valid(add_aministrator_facade: AdministratorFacade,
                                               new_admin_valid, new_user_not_valid_user_email):
    try:
        add_aministrator_facade.add_administrator(new_admin_valid, new_user_not_valid_user_email)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_administrator_neg_firstname_empty(add_aministrator_facade: AdministratorFacade,
                                               new_admin_valid, new_administrator_user):
    try:
        new_admin_valid.first_name = ''
        add_aministrator_facade.add_administrator(new_admin_valid, new_administrator_user)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.ADMIN_FIRST_NAME:
            assert False, f'test falied: not EMPTY/ADMIN_FIRST_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_administrator_neg_lastname_empty(add_aministrator_facade: AdministratorFacade,
                                              new_admin_valid, new_administrator_user):
    try:
        new_admin_valid.last_name = ''
        add_aministrator_facade.add_administrator(new_admin_valid, new_administrator_user)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.EMPTY or inner.field_name != Field.ADMIN_LAST_NAME:
            assert False, f'test falied: not EMPTY/ADMIN_LAST_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# def test_add_administrator_neg_user_id_empty(add_aministrator_facade: AdministratorFacade,
#                                              new_admin_valid, new_administrator_user):
#     try:
#         new_admin_valid.user_id = None
#         add_aministrator_facade.add_administrator(new_admin_valid, new_administrator_user)
#         assert False
#     except FlightSystemException as exc:
#         inner = GenericService.get_root_exception(exc)
#         if not isinstance(inner, NotVaildInputException):
#             assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
#         if inner.cause != Reason.EMPTY or inner.field_name != Field.ADMIN_USER_ID:
#             assert False, f'test falied: not EMPTY/AIRLINE_USER_ID NotVaildInputException exception'
#         assert True
#     except Exception as exc:
#         assert False, f'test failed because of an exception : {str(exc)}'
#

def test_add_administrator_neg_firstname_too_long(add_aministrator_facade: AdministratorFacade,
                                                  new_admin_valid, new_administrator_user):
    new_admin_valid.first_name = ('D' * (Administrator.FIRST_NAME_MAX + 1))
    try:
        add_aministrator_facade.add_administrator(new_admin_valid, new_administrator_user)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.TOO_LONG or inner.field_name != Field.ADMIN_FIRST_NAME:
            assert False, f'test falied: not EMPTY/AIRLINE_USER_ID NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_add_administrator_neg_lastname_too_long(add_aministrator_facade: AdministratorFacade,
                                                 new_admin_valid, new_administrator_user):
    new_admin_valid.last_name = ('D' * (Administrator.LAST_NAME_MAX + 1))
    try:
        add_aministrator_facade.add_administrator(new_admin_valid, new_administrator_user)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotVaildInputException):
            assert False, f'test falied: not NotVaildInputException exception: {str(inner)}'
        if inner.cause != Reason.TOO_LONG or inner.field_name != Field.ADMIN_LAST_NAME:
            assert False, f'test falied: not EMPTY/ADMIN_LAST_NAME NotVaildInputException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


# def test_add_administrator_neg_user_id_not_exists(add_aministrator_facade: AdministratorFacade,
#                                                   new_admin_valid, new_administrator_user):
#     new_admin_valid.user_id = 0
#     try:
#         add_aministrator_facade.add_administrator(new_admin_valid, new_administrator_user)
#         assert False
#     except FlightSystemException as exc:
#         inner = GenericService.get_root_exception(exc)
#         if not isinstance(inner, NotFoundException):
#             assert False, f'test falied: not NotFoundException exception: {str(inner)}'
#         if inner.entity != Entity.USER:
#             assert False, f'test falied: not USER NotFoundException exception'
#         assert True
#     except Exception as exc:
#         assert False, f'test failed because of an exception : {str(exc)}'


# ***********************************************************
# REMOVE ADMINISRATOR
@pytest.fixture
def remove_aministrator_facade(facade: AnonymousFacade, exists_administrator):
    admin_facade = facade.login(exists_administrator['username'], exists_administrator['password'])
    return admin_facade


@pytest.fixture
def admin_id_to_remove():
    return 1


def test_remove_administrator_positive(remove_aministrator_facade: AdministratorFacade, admin_id_to_remove):
    try:
        remove_aministrator_facade.remove_administrator(admin_id_to_remove)
    except Exception as exc:
        assert False, f'exception raised, {str(exc)}'
    try:
        administrator = remove_aministrator_facade.get_administrator_by_id(admin_id_to_remove)
        if administrator is not None:
            assert False, f'administrator removed but administrator returns'
        assert True
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException'
        if inner.entity != Entity.ADMINISTRATOR:
            assert False, f'test falied: not ADMINISTRATOR NotFoundException'
        assert True
    except Exception as exc:
        assert False, f'exception raised (only in test code), {str(exc)}'


def test_remove_administrator_neg_invalid_token(remove_aministrator_facade: AdministratorFacade):
    try:
        invalid_token_admin_id = 2
        remove_aministrator_facade.remove_administrator(invalid_token_admin_id)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, InvalidTokenException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'


def test_remove_administrator_neg_admin_not_found(remove_aministrator_facade: AdministratorFacade):
    try:
        admin_id_not_found = -999
        remove_aministrator_facade.remove_administrator(admin_id_not_found)
        assert False
    except FlightSystemException as exc:
        inner = GenericService.get_root_exception(exc)
        if not isinstance(inner, NotFoundException):
            assert False, f'test falied: not NotFoundException exception: {str(inner)}'
        if inner.entity != Entity.ADMINISTRATOR:
            assert False, f'test falied: not ADMINISTRATOR NotFoundException exception'
        assert True
    except Exception as exc:
        assert False, f'test failed because of an exception : {str(exc)}'
