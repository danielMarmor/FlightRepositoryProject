from common.entities.Flight import Flight
from business.services.validationService import ValidationService
from common.entities.AirlineCompany import AirlineCompany
from common.constants.enums import Entity, Reason, Field, Actions, TicketBalanceOperation
from common.exceptions.notValidInputException import NotVaildInputException
from common.exceptions.notValidFlightException import NotValidFlightException
from common.entities.User import User
from common.entities.Country import Country
from common.entities.Administrator import Administrator
from business.services.loginService import LoginService
from common.exceptions.notFoundException import NotFoundException
from common.exceptions.notUniqueException import NotUniqueException
from sqlalchemy.sql.operators import is_
from sqlalchemy import or_, and_



class AirlineService:
    ALL = -1
    ALL_STR = '-1'

    def __init__(self, local_session, repository):
        self.login_service = LoginService(local_session, repository)
        self._repository = repository

    def get_all_flights(self):
        flights = self._repository.get_all(Flight)
        return flights

    def get_flight_by_id(self, flight_id):
        flight = self._repository.get_by_id(Flight, flight_id)
        if flight is None:
            raise NotFoundException('Flight Not Found', Entity.FLIGHT, flight_id)
        return flight

    def get_flights_by_airline(self, airline_id):
        airline = self.get_airline_by_id(airline_id)
        if airline is None:
            raise NotFoundException('Airline Not Found', Entity.AIRLINE_COMPANY, airline_id)
        flights = self._repository.get_flights_by_airline_id(airline_id)
        return flights

    def get_airlines_by_parameters(self, country_id, name):
        serach_country_id = self.ALL if country_id is None else country_id
        search_name = self.ALL_STR if name is None else '%{}%'.format(name)
        airlines_cond = (lambda query: query.filter(
                and_(or_(serach_country_id == self.ALL, AirlineCompany.country_id == country_id),
                     or_(search_name == self.ALL_STR, AirlineCompany.name.like(search_name)))))
        airlines = self._repository.get_all_by_condition(AirlineCompany, airlines_cond)
        return airlines

    def get_flights_by_params(self, origin_country_id, dest_country_id, start_date, end_date):
        flights = self._repository.get_flights_by_parameters(origin_country_id, dest_country_id, start_date, end_date)
        return flights

    @staticmethod
    def check_flight_params(origin_country_id, dest_country_id, start_date, end_date):
        is_valid_date = ValidationService.validate_date(start_date)
        if not is_valid_date:
            raise NotVaildInputException('Not Valid Start Date', Reason.NOT_VALID_DATE, Field.FLIGHT_DEPARTURE_DATE)
        is_valid_date = ValidationService.validate_date(end_date)
        if not is_valid_date:
            raise NotVaildInputException('Not Valid End Date', Reason.NOT_VALID_DATE, Field.FLIGHT_LANDING_DATE)

    def get_all_airlines(self):
        airlines = self._repository.get_all(AirlineCompany)
        return airlines

    def get_airline_by_id(self, airline_id):
        airline = self._repository.get_by_id(AirlineCompany, airline_id)
        return airline

    def validate_airline(self, airline: AirlineCompany):
        # is empty
        empty_name = not ValidationService.validate_not_empty(airline.name)
        if empty_name:
            raise NotVaildInputException('Empty Name!', Reason.EMPTY, Field.AIRLINE_COMPANY_NAME)
        empty_country_id = not ValidationService.validate_not_null(airline.country_id)
        if empty_country_id:
            raise NotVaildInputException('Empty Country Id!', Reason.EMPTY, Field.AIRLINE_COUNTRY_ID)
        # empty_user_id ==> CHECK ONLY ON UPDATE
        if airline.id is not None:
            empty_user_id = not ValidationService.validate_not_null(airline.user_id)
            if empty_user_id:
                raise NotVaildInputException('Empty User Id!', Reason.EMPTY, Field.AIRLINE_USER_ID)
        # is name to long :
        name_not_valid = not ValidationService.validate_max_lenght(airline.name, AirlineCompany.MAX_NAME)
        if name_not_valid:
            raise NotVaildInputException('Name is Too Long', Reason.TOO_LONG, Field.AIRLINE_COMPANY_NAME)

        # country
        country = self._repository.get_by_id(Country, airline.country_id)
        if country is None:
            raise NotFoundException('Country Not Found', Entity.COUNTRY, airline.country_id)

        # user ==> CHECK ONLY ON UPDATE
        if airline.id is not None:
            user = self._repository.get_by_id(User, airline.user_id)
            if user is None:
                raise NotFoundException('User Not Found', Entity.USER, airline.user_id)

        # unique constraints violation - name
        not_unique_name_airline_cond = \
            (lambda query: query.filter(AirlineCompany.name == airline.name,
                                        AirlineCompany.id != airline.id))
        not_unique_name_airline = self._repository.get_all_by_condition(AirlineCompany, not_unique_name_airline_cond)
        if len(not_unique_name_airline) > 0:
            raise NotUniqueException('Name Already Exists!',
                                     Actions.ADD_AIRLINE if airline.id is None else Actions.UPDATE_AIRLINE,
                                     Field.AIRLINE_COMPANY_NAME,
                                     airline.name)

    @staticmethod
    def validate_flight(flight):
        # is empty
        empty_airline_company = not ValidationService.validate_not_null(flight.airline_company_id)
        if empty_airline_company:
            raise NotVaildInputException('Airline Id Null!', Reason.EMPTY, Field.FLIGHT_AIRLINE_ID)
        empty_origin_country_id = not ValidationService.validate_not_null(flight.origin_country_id)
        if empty_origin_country_id:
            raise NotVaildInputException('Origin Country_id Null!', Reason.EMPTY, Field.FLIGHT_ORIGIN_COUNTRY_ID)
        empty_dest_country_id = not ValidationService.validate_not_null(flight.destination_country_id)
        if empty_dest_country_id:
            raise NotVaildInputException('Detination Country_id Null!', Reason.EMPTY, Field.FLIGHT_DEST_COUNTRY_ID)
        empty_departure_date = not ValidationService.validate_not_null(flight.departure_time)
        if empty_departure_date:
            raise NotVaildInputException('departure_time Null!', Reason.EMPTY, Field.FLIGHT_DEPARTURE_DATE)
        empty_landing_date = not ValidationService.validate_not_null(flight.landing_time)
        if empty_landing_date:
            raise NotVaildInputException('landing_time Null!', Reason.EMPTY, Field.FLIGHT_LANDING_DATE)

        # mismatch daparture-landing times
        if flight.departure_time > flight.landing_time:
            raise NotValidFlightException('Departure Time is later than Landing Time',
                                          Reason.DEPARTURE_LANDING_MISMATCH)

        # same country flight
        if flight.destination_country_id == flight.origin_country_id:
            raise NotValidFlightException('Destination Country Same as Origin Country',
                                              Reason.SAME_COUNTRY_FLIGHT)

        # not positive tickets balance
        if flight.remaining_tickets <= 0:
            raise NotValidFlightException('Remainig Tickets must be grater than 0',
                                          Reason.REMAING_TICKETS_INVALID)

    def add_airline(self, airline, user):
        self._repository.add_airline(airline, user)

    def update_airline(self, user_id, user, airline_id, airline):
        self._repository.update_airline(user_id, user, airline_id, airline)

    def remove_airline(self, airline_id):
        airline = self.get_airline_by_id(airline_id)
        if airline is None:
            raise NotFoundException('Airline Company Not Found', Entity.AIRLINE_COMPANY, airline_id)
        self._repository.remove_airline(airline_id)

    def add_fligth(self, flight):
        self._repository.add(flight)

    def update_fligth(self, flight_id, flight):
        update_data_filter = {
            'airline_company_id': flight.airline_company_id,
            'origin_country_id': flight.origin_country_id,
            'destination_country_id': flight.destination_country_id,
            'departure_time': flight.departure_time,
            'landing_time': flight.landing_time,
            'remaining_tickets': flight.remaining_tickets
        }
        self._repository.update(Flight, 'id', flight_id, update_data_filter)

    def remove_flight(self, flight_id):
        self._repository.remove_flight(flight_id)

    def update_fligth_tickets(self, flight_id, flight, ticket_balance_operation):
        remaining_tickets = None
        if ticket_balance_operation == TicketBalanceOperation.REMOVE_TICKET:
            remaining_tickets = flight.remaining_tickets - 1
        else:  # ticket_balance_operation == TicketBalanceOperation.ADD_TICKET:
            remaining_tickets = flight.remaining_tickets + 1
        updated_data_filter = {'remaining_tickets': remaining_tickets}
        self._repository.update(Flight, 'id', flight_id, updated_data_filter)

    def get_administrator_by_id(self, administrator_id):
        administrator = self._repository.get_by_id(Administrator, administrator_id)
        return administrator

    def validate_administrator(self, administrator: Administrator):
        # EMPTY ==>
        empty_first_name = not ValidationService.validate_not_empty(administrator.first_name)
        if empty_first_name:
            raise NotVaildInputException('first_name Empty!', Reason.EMPTY, Field.ADMIN_FIRST_NAME)
        empty_last_name = not ValidationService.validate_not_empty(administrator.last_name)
        if empty_last_name:
            raise NotVaildInputException('last_name Empty!', Reason.EMPTY, Field.ADMIN_LAST_NAME)
        empty_user_id = not ValidationService.validate_not_null(administrator.user_id)
        # if empty_user_id:
        #     raise NotVaildInputException('first_name Empty!', Reason.EMPTY, Field.ADMIN_USER_ID)
        # TO LONG ==>
        too_log_first_name = \
            not ValidationService.validate_max_lenght(administrator.first_name, Administrator.FIRST_NAME_MAX)
        if too_log_first_name:
            raise NotVaildInputException('First Name too Long', Reason.TOO_LONG, Field.ADMIN_FIRST_NAME)
        too_log_last_name = \
            not ValidationService.validate_max_lenght(administrator.last_name, Administrator.LAST_NAME_MAX)
        if too_log_last_name:
            raise NotVaildInputException('Last Name too Long', Reason.TOO_LONG, Field.ADMIN_LAST_NAME)
        # USER
        # user_by_admin_user_id_cond = (lambda query: query.filter(User.id == administrator.user_id))
        # user_by_admin_user_id = self._repository.get_all_by_condition(User, user_by_admin_user_id_cond)
        # if len(user_by_admin_user_id) == 0:
        #     raise NotFoundException('User not Found', Entity.USER, administrator.user_id)

    def remove_administrator(self, administrator_id):
        self._repository.remove_administrator(administrator_id)

    def add_administrator(self, administrator, user):
        self._repository.add_administrator(administrator, user)

    def get_all_countries(self):
        countries = self._repository.get_all(Country)
        return countries

    def get_country_by_id(self, country_id):
        country = self._repository.get_by_id(Country, country_id)
        return country

    def add_country(self, new_country):
        self._repository.add(new_country)

    def get_country_by_name(self, name):
        country_cond = (lambda query: query.filter(Country.name == name))
        countries = self._repository.get_all_by_condition(Country, country_cond)
        return countries
