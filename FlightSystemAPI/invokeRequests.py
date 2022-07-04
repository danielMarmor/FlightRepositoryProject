import threading
from common.constants.enums import Actions
from business.facade.anonymousFacade import AnonymousFacade
from business.facade.administratorFacade import AdministratorFacade
from business.facade.customerFacade import CustomerFacade
from business.facade.airlineFacade import AirlineFacade
from common.entities.User import User
from common.entities.Customer import Customer
from common.entities.AirlineCompany import AirlineCompany
from common.entities.Administrator import Administrator
from common.entities.Ticket import Ticket
from common.not_mapped.identityToken import IdentityToken
from common.entities.Flight import Flight
from business.services.genericService import GenericService


class InvokeRequests:
    MAX_FLIGHT_TICKETS = 40

    def __init__(self, db_session):
        self.lock = threading.RLock()
        self.db_session = db_session

    def invoke(self, facade_name, action_id, data):
        with self.lock:
            match facade_name:
                case 'anonym': return self.invoke_anonym(action_id, data)
                case 'admin': return self.invoke_admin(action_id, data)
                case 'airline': return self.invoke_airline(action_id, data)
                case 'cust': return self.invoke_customer(action_id, data)

    def invoke_anonym(self, action_id, data):
        facade = AnonymousFacade(self.db_session)
        response = None
        match action_id:
            case Actions.GET_ALL_FLIGHTS:
                response = facade.get_all_flights()
            case Actions.GET_FLIGHT_BY_ID:
                flight_id = data['id']
                response = facade.get_flight_by_id(flight_id)
            case Actions.GET_ALL_AIRLINES:
                response = facade.get_all_airlines()
            case Actions.GET_AIRLINE_BY_ID:
                airline_id = data['id']
                response = facade.get_airline_by_id(airline_id)
            case Actions.GET_AIRLINES_BY_PARAMS:
                country_id = data['country_id']
                name = data['name']
                response = facade.get_airlines_by_parameters(country_id, name)
            case Actions.GET_ALL_COUNTRIES:
                response = facade.get_all_countries()
            case Actions.LOGIN:
                username = data['username']
                password = data['password']
                response = facade.login(username, password)
            case Actions.ADD_CUSTOMER:
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                customer = Customer(id=data['customer']['id'],
                                    first_name=data['customer']['first_name'],
                                    last_name=data['customer']['last_name'],
                                    address=data['customer']['address'],
                                    phone_number=data['customer']['phone_number'],
                                    credit_card_number=data['customer']['credit_card_number'],
                                    user_id=data['customer']['user_id'])
                facade.add_customer(customer, user)
                response = None
            case Actions.GET_ALL_USERS:
                response = facade.get_all_customers_users()
            case Actions.GET_TICKETS_BY_USER:
                email = data['email']
                response = facade.get_tickets_by_username(email)
        return response

    def invoke_admin(self, action_id, data):
        token = IdentityToken(data['token']['user_name'],
                              data['token']['user_role_id'],
                              data['token']['identity_id'])
        facade = AdministratorFacade(self.db_session, token)
        response = None
        match action_id:
            case Actions.GET_ALL_FLIGHTS:
                response = facade.get_all_flights()
            case Actions.GET_FLIGHT_BY_ID:
                flight_id = data['id']
                response = facade.get_flight_by_id(flight_id)
            case Actions.GET_ALL_AIRLINES:
                response = facade.get_all_airlines()
            case Actions.GET_AIRLINE_BY_ID:
                airline_id = data['id']
                response = facade.get_airline_by_id(airline_id)
            case Actions.GET_AIRLINES_BY_PARAMS:
                country_id = data['country_id']
                name = data['name']
                response = facade.get_airlines_by_parameters(country_id, name)
            case Actions.GET_ALL_COUNTRIES:
                response = facade.get_all_countries()
            case Actions.GET_ALL_CUSTOMERS:
                response = facade.get_all_customers()
            case Actions.ADD_CUSTOMER:
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                customer = Customer(id=data['customer']['id'],
                                    first_name=data['customer']['first_name'],
                                    last_name=data['customer']['last_name'],
                                    address=data['customer']['address'],
                                    phone_number=data['customer']['phone_number'],
                                    credit_card_number=data['customer']['credit_card_number'],
                                    user_id=data['customer']['user_id'])
                facade.add_customer(customer, user)
                response = None
            case Actions.REMOVE_CUSTOMER:
                customer_id = data['customer_id']
                facade.remove_customer(customer_id)
                response = None
            case Actions.ADD_AIRLINE:
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                airline = AirlineCompany(id=data['airline']['id'],
                                         name=data['airline']['name'],
                                         country_id=data['airline']['country_id'],
                                         user_id=data['airline']['user_id'])
                facade.add_airline(airline, user)
                response = None
            case Actions.REMVOE_AIRLINE:
                airline_id = data['airline_id']
                facade.remove_airline(airline_id)
                response = None
            case Actions.ADD_ADMINISTRATOR:
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                admin = Administrator(id=data['administrator']['id'],
                                         first_name=data['administrator']['first_name'],
                                         last_name=data['administrator']['last_name'],
                                         user_id=data['administrator']['user_id'])
                facade.add_administrator(admin, user)
                response = None
            case Actions.REMOVE_ADMINISTRATOR:
                administrator_id = data['administrator_id']
                facade.remove_administrator(administrator_id)
                response = None
        return response

    def invoke_airline(self, action_id, data):
        token = IdentityToken(data['token']['user_name'],
                              data['token']['user_role_id'],
                              data['token']['identity_id'])
        facade = AirlineFacade(self.db_session, token)
        response = None
        match action_id:
            case Actions.GET_ALL_FLIGHTS:
                response = facade.get_all_flights()
            case Actions.GET_FLIGHT_BY_ID:
                flight_id = data['id']
                response = facade.get_flight_by_id(flight_id)
            case Actions.GET_ALL_AIRLINES:
                response = facade.get_all_airlines()
            case Actions.GET_AIRLINE_BY_ID:
                airline_id = data['id']
                response = facade.get_airline_by_id(airline_id)
            case Actions.GET_AIRLINES_BY_PARAMS:
                country_id = data['country_id']
                name = data['name']
                response = facade.get_airlines_by_parameters(country_id, name)
            case Actions.GET_ALL_COUNTRIES:
                response = facade.get_all_countries()
            case Actions.GET_FLIGHT_BY_AIRLINE:
                airline_id = data['airline_id']
                response_data = facade.get_my_flights(airline_id)
                data_props = ('flight_id', 'airline_company_id', 'airline_company_name', 'origin_country_id',\
                              'origin_country_name', 'destination_country_id', 'dest_country_name',\
                              'departure_time', 'landing_time', 'remaining_tickets')
                response = GenericService.wrap_list_dict(response_data, data_props)
            case Actions.UPDATE_AIRLINE:
                anonym_facade = AnonymousFacade(self.db_session)
                airline_id = data['airline_id']
                user = anonym_facade.get_user_by_user_name(token.user_name)
                airline = AirlineCompany(id=data['airline']['id'],
                                         name=data['airline']['name'],
                                         country_id=data['airline']['country_id'],
                                         user_id=user.id)
                facade.update_airline(airline_id, airline)
                response = None
            case Actions.ADD_FLIGHT:
                flight = Flight(id=data['flight']['id'],
                                airline_company_id=data['flight']['airline_company_id'],
                                origin_country_id=data['flight']['origin_country_id'],
                                destination_country_id=data['flight']['destination_country_id'],
                                departure_time=GenericService.compose_datetime(
                                    data['flight']['departure_date'],
                                    data['flight']['departure_hour'],
                                    data['flight']['departure_minute'], '-'),
                                landing_time=GenericService.compose_datetime(
                                    data['flight']['landing_date'],
                                    data['flight']['landing_hour'],
                                    data['flight']['landing_minute'], '-'),
                                remaining_tickets=self.MAX_FLIGHT_TICKETS)
                facade.add_flight(flight)
                response = None
            case Actions.UPDATE_FLIGHT:
                flight_id = data['flight_id']
                flight = Flight(id=data['flight']['id'],
                                airline_company_id=data['flight']['airline_company_id'],
                                origin_country_id=data['flight']['origin_country_id'],
                                destination_country_id=data['flight']['destination_country_id'],
                                departure_time=GenericService.compose_datetime(
                                    data['flight']['departure_date'],
                                    data['flight']['departure_hour'],
                                    data['flight']['departure_minute'], '-'),
                                landing_time=GenericService.compose_datetime(
                                    data['flight']['landing_date'],
                                    data['flight']['landing_hour'],
                                    data['flight']['landing_minute'], '-'),
                                remaining_tickets=data['flight']['remaining_tickets'])
                facade.update_flight(flight_id, flight)
                response = None
            case Actions.REMOVE_FLIGHT:
                fligth_id = data['flight_id']
                facade.remove_flight(fligth_id)
                response = None
        return response

    def invoke_customer(self, action_id, data):
        token = IdentityToken(data['token']['user_name'],
                              data['token']['user_role_id'],
                              data['token']['identity_id'])
        facade = CustomerFacade(self.db_session, token)
        response = None
        match action_id:
            case Actions.GET_ALL_FLIGHTS:
                response = facade.get_all_flights()
            case Actions.GET_FLIGHT_BY_ID:
                flight_id = data['id']
                response = facade.get_flight_by_id(flight_id)
            case Actions.GET_ALL_AIRLINES:
                response = facade.get_all_airlines()
            case Actions.GET_AIRLINE_BY_ID:
                airline_id = data['id']
                response = facade.get_airline_by_id(airline_id)
            case Actions.GET_AIRLINES_BY_PARAMS:
                country_id = data['country_id']
                name = data['name']
                response = facade.get_airlines_by_parameters(country_id, name)
            case Actions.GET_ALL_COUNTRIES:
                response = facade.get_all_countries()
            case Actions.UPDATE_CUSTOMER:
                anonym_facade = AnonymousFacade(self.db_session)
                user = anonym_facade.get_user_by_user_name(token.user_name)
                customer_id = data['customer_id']
                customer = Customer(id=data['customer']['id'],
                                    first_name=data['customer']['first_name'],
                                    last_name=data['customer']['last_name'],
                                    address=data['customer']['address'],
                                    phone_number=data['customer']['phone_number'],
                                    credit_card_number=data['customer']['credit_card_number'],
                                    user_id=user.id)
                facade.update_customer(customer_id, customer)
                response = None
            case Actions.ADD_TICKET:
                ticket = Ticket(
                    flight_id=data['ticket']['flight_id'],
                    customer_id=data['ticket']['customer_id']
                )
                facade.add_ticket(ticket)
                response = None
            case Actions.REMOVE_TICKET:
                ticket_id = data['ticket_id']
                facade.remove_ticket(ticket_id)
                response = None
            case Actions.GET_TICKETS_BY_CUSTOMER:
                customer_id = data['customer_id']
                res_data = facade.get_my_tickets(customer_id)
                data_props = ('ticket_id', 'flight_id', 'customer_id')
                response = GenericService.wrap_list_dict(res_data, data_props)
        return response





