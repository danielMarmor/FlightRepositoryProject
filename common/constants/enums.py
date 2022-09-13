from enum import IntEnum


class Entity(IntEnum):
    USER_ROLES = 1,
    ADMINISTRATOR = 2,
    USER = 3,
    AIRLINE_COMPANY = 4,
    FLIGHT = 5,
    CUSTOMER = 6,
    TICKET = 7,
    COUNTRY = 8,
    IDENTITY_TOKEN = 9


class UserRoles(IntEnum):
    CUSTOMER = 1
    AIRLINE = 2,
    ADMINISTATOR = 3


class UserLoginErrorProperties(IntEnum):
    USERNAME = 1,
    PASSWORD = 2,
    EMAIL = 3


# for empty data Exception required field detection
class RequiredField(IntEnum):
    USERNAME = 1,
    PASSWORD = 2,
    EMAIL = 3,
    FIRST_NAME = 4,
    LAST_NAME = 5,
    ADDRESS = 6,
    PHONE = 7,
    CREDIT_CARD = 8


class Reason(IntEnum):
    EMPTY = 1
    TOO_LONG = 2,
    TOO_SHORT = 3
    NOT_FORMATTED = 4,
    DEPARTURE_LANDING_MISMATCH = 5,
    REMAING_TICKETS_INVALID = 6,
    CROSS_FLIGHT = 7,
    NOT_VALID_DATE = 8
    FLIGHT_ALLREADY_DEPARTURED = 9,
    FLIGHT_SOLD_OUT = 10,
    SAME_COUNTRY_FLIGHT = 11,
    NUM_SEATS_INVALID = 12,
    DISTANCE_INVALID = 13


class Field(IntEnum):
    CUSTOMER_ID = 1,
    CUSTOMER_USER_ID = 2,
    CUSTOMER_FIRST_NAME = 3,
    CUSTOMER_LAST_NAME = 4,
    CUSTOMER_ADDRESS_NAME = 5,
    CUSTOMER_PHONE_NAME = 6,
    CUSTOMER_CREDIT_CARD = 7,
    AIRLINE_COMPANY_ID = 8,
    AIRLINE_COMPANY_NAME = 9,
    AIRLINE_COUNTRY_ID = 10,
    AIRLINE_USER_ID = 11,
    FLIGHT_AIRLINE_ID = 12,
    FLIGHT_ORIGIN_COUNTRY_ID = 13,
    FLIGHT_DEST_COUNTRY_ID = 14,
    FLIGHT_DEPARTURE_DATE = 15,
    FLIGHT_LANDING_DATE = 16,
    FLIGHT_REMAIN_TICKETS = 17,
    ADMIN_FIRST_NAME = 18,
    ADMIN_LAST_NAME = 19,
    ADMIN_USER_ID = 20,
    USER_NAME = 21,
    USER_PASSWORD = 22,
    USER_EMAIL = 23,
    USER_ROLE_ID = 24


class Actions(IntEnum):
    LOGIN = 1,
    CREATE_NEW_USER = 2,
    GET_ALL_FLIGHTS = 3,
    GET_FLIGHT_BY_ID = 4,
    GET_FLIGHT_BY_PARAMS = 5,
    GET_ALL_AIRLINES = 6,
    GET_AIRLINE_BY_ID = 7,
    GET_CUSTOMER_BY_ID = 8,
    ADD_CUSTOMER = 9,
    UPDATE_CUSTOMER = 10,
    REMOVE_CUSTOMER = 11,
    ADD_TICKET = 12,
    REMOVE_TICKET = 13,
    GET_TICKETS_BY_CUSTOMER = 14,
    ADD_AIRLINE = 15,
    UPDATE_AIRLINE = 16,
    REMVOE_AIRLINE = 17,
    ADD_FLIGHT = 18,
    UPDATE_FLIGHT = 19,
    REMOVE_FLIGHT = 20,
    ADD_ADMINISTRATOR = 21,
    REMOVE_ADMINISTRATOR = 22,
    GET_ALL_CUSTOMERS = 23,
    GET_ALL_COUNTRIES = 24,
    GET_COUNTRY_BY_ID = 25,
    GET_FLIGHT_BY_AIRLINE = 26,
    GET_AIRLINES_BY_PARAMS = 27,
    GET_ALL_USERS = 28,
    GET_TICKETS_BY_USER = 29,
    GET_CUSTOMERS_BY_PARAMS = 30,
    GET_CUSTOMERS_BUSINNES_DATA = 31,
    GET_AIRLINES_BUSINNES_DATA = 32,
    GET_ADMINISTRATORS_BY_PARAMS = 33,
    GET_ADMINISTRATOR_BY_ID = 34,
    UPDATE_ADMINISTRATOR = 35,
    GET_TICKETS_BY_FLIGHT = 36,
    GET_SALES_DAILY_DATA = 37,
    GET_PURCHASES_BY_CUSTOMERS = 38,
    GET_SALES_BY_AIRLINES = 39,
    GET_COUNT_FLIGHTS = 40,
    GET_CAPACITIES_UTIL = 41,
    CHECK_TICKET = 42,
    UPDATE_ADMINISTRATOR_BY_PEER = 43



class TicketBalanceOperation(IntEnum):
    ADD_TICKET = 1,
    REMOVE_TICKET = 2


class DbGenerationOpetion(IntEnum):
    ADD = 1,
    REPLACE = 2




