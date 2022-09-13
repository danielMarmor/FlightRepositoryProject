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

            case Actions.GET_FLIGHT_BY_PARAMS:
                origin_country_id = data['origin_country_id']
                dest_country_id = data['dest_country_id']
                start_date = data['start_date']
                end_date = data['end_date']
                response = facade.get_flights_by_parameters(origin_country_id, dest_country_id, start_date, end_date)

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
                                    image_url=data['customer']['image_url'],
                                    user_id=data['customer']['user_id'])
                response = facade.add_customer(customer, user)

            case Actions.ADD_AIRLINE:
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                airline = AirlineCompany(id=data['airline']['id'],
                                         name=data['airline']['name'],
                                         country_id=data['airline']['country_id'],
                                         iata=data['airline']['iata'],
                                         user_id=data['airline']['user_id'])
                response = facade.add_airline(airline, user)

            case Actions.GET_ALL_USERS:
                response = facade.get_all_customers_users()

            case Actions.GET_TICKETS_BY_USER:
                email = data['email']
                response = facade.get_tickets_by_username(email)
        return response

    def invoke_admin(self, action_id, data):
        token = None
        # token = IdentityToken(data['token']['user_name'],
        #                       data['token']['user_role_id'],
        #                       data['token']['identity_id'])
        facade = AdministratorFacade(self.db_session, token)
        response = None
        match action_id:
            case Actions.GET_ALL_FLIGHTS:
                response = facade.get_all_flights()

            case Actions.GET_FLIGHT_BY_ID:
                flight_id = data['id']
                response = facade.get_flight_by_id(flight_id)

            case Actions.GET_FLIGHT_BY_PARAMS:
                origin_country_id = data['origin_country_id']
                dest_country_id = data['dest_country_id']
                start_date = data['start_date']
                end_date = data['end_date']
                response = facade.get_flights_by_parameters(origin_country_id, dest_country_id, start_date, end_date)

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

            case Actions.GET_CUSTOMERS_BY_PARAMS:
                search = data['search']
                response = facade.get_customers_by_params(search)

            case Actions.GET_CUSTOMER_BY_ID:
                customer_id = data['customer_id']
                response = facade.get_customer_by_id(customer_id)

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
                                    image_url=data['customer']['image_url'],
                                    user_id=data['customer']['user_id'])
                new_customer = facade.add_customer(customer, user)
                response = new_customer

            case Actions.UPDATE_CUSTOMER:
                customer_id = data['customer_id']
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
                                    image_url=data['customer']['image_url'],
                                    user_id=data['customer']['user_id'])
                facade.update_customer(customer_id, customer, user)
                response = {'success': 'OK'}

            case Actions.REMOVE_CUSTOMER:
                customer_id = data['customer_id']
                facade.remove_customer(customer_id)
                response = {'success': 'OK'}

            case Actions.ADD_AIRLINE:
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                airline = AirlineCompany(id=data['airline']['id'],
                                         name=data['airline']['name'],
                                         country_id=data['airline']['country_id'],
                                         iata=data['airline']['iata'],
                                         user_id=data['airline']['user_id'])
                new_airline = facade.add_airline(airline, user)
                response = new_airline

            case Actions.UPDATE_AIRLINE:
                airline_id = data['airline_id']
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                airline = AirlineCompany(id=data['airline']['id'],
                                         name=data['airline']['name'],
                                         country_id=data['airline']['country_id'],
                                         iata=data['airline']['iata'],
                                         user_id=data['airline']['user_id'])
                facade.update_airline(airline_id, airline, user)
                response = {'success': 'OK'}

            case Actions.GET_ADMINISTRATOR_BY_ID:
                administrator_id = data['administrator_id']
                response = facade.get_administrator_by_id(administrator_id)

            case Actions.REMVOE_AIRLINE:
                airline_id = data['airline_id']
                facade.remove_airline(airline_id)
                response = {'success': 'OK'}

            case Actions.ADD_ADMINISTRATOR:
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                admin = Administrator(id=data['administrator']['id'],
                                         first_name=data['administrator']['first_name'],
                                         last_name=data['administrator']['last_name'],
                                         user_id=data['administrator']['user_id'],
                                         image_url = data['administrator']['image_url'])
                new_admin = facade.add_administrator(admin, user)
                response = new_admin

            case Actions.UPDATE_ADMINISTRATOR:
                administrator_id =  data['administrator_id']
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                admin = Administrator(id=data['administrator']['id'],
                                      first_name=data['administrator']['first_name'],
                                      last_name=data['administrator']['last_name'],
                                      user_id=data['administrator']['user_id'],
                                      image_url = data['administrator']['image_url'])
                admin_data = facade.update_administrator(administrator_id, admin, user)
                response = admin_data

            case Actions.UPDATE_ADMINISTRATOR_BY_PEER:
                administrator_id = data['administrator_id']
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                admin = Administrator(id=data['administrator']['id'],
                                      first_name=data['administrator']['first_name'],
                                      last_name=data['administrator']['last_name'],
                                      user_id=data['administrator']['user_id'],
                                      image_url=data['administrator']['image_url'])
                admin_data = facade.update_administrator(administrator_id, admin, user)
                response = admin_data

            case Actions.REMOVE_ADMINISTRATOR:
                administrator_id = data['administrator_id']
                facade.remove_administrator(administrator_id)
                response = {'success': 'OK'}

            case Actions.GET_CUSTOMERS_BUSINNES_DATA:
                search = data['search']
                response = facade.get_customers_bussines_data(search)

            case Actions.GET_AIRLINES_BUSINNES_DATA:
                search = data['search']
                response = facade.get_airlines_bussines_data(search)

            case Actions.GET_ADMINISTRATORS_BY_PARAMS:
                search = data['search']
                response = facade.get_administrators_by_params(search)

            case Actions.GET_SALES_DAILY_DATA:
                start_date = data['start_date']
                end_date = data['end_date']
                destination_country_id = data['destination_country_id']
                response = facade.get_daily_sales_data(start_date, end_date, destination_country_id);

            case Actions.GET_PURCHASES_BY_CUSTOMERS:
                start_date = data['start_date']
                end_date = data['end_date']
                destination_country_id = data['destination_country_id']
                response = facade.get_purchases_by_customers(start_date, end_date, destination_country_id);

            case Actions.GET_SALES_BY_AIRLINES:
                start_date = data['start_date']
                end_date = data['end_date']
                destination_country_id = data['destination_country_id']
                response = facade.get_sales_by_airlines(start_date, end_date, destination_country_id);

            case Actions.GET_COUNT_FLIGHTS:
                start_date = data['start_date']
                end_date = data['end_date']
                destination_country_id = data['destination_country_id']
                response = facade.get_count_flights(start_date, end_date, destination_country_id);

            case Actions.GET_CAPACITIES_UTIL:
                start_date = data['start_date']
                end_date = data['end_date']
                destination_country_id = data['destination_country_id']
                response = facade.get_capacities_util(start_date, end_date, destination_country_id);

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

            case Actions.GET_FLIGHT_BY_PARAMS:
                origin_country_id = data['origin_country_id']
                dest_country_id = data['dest_country_id']
                start_date = data['start_date']
                end_date = data['end_date']
                response = facade.get_flights_by_parameters(origin_country_id, dest_country_id, start_date, end_date)

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
                response = facade.get_my_flights(airline_id)

            case Actions.UPDATE_AIRLINE:
                airline_id = data['airline_id']
                user = User(id=data['user']['id'],
                            username=data['user']['username'],
                            password=data['user']['password'],
                            email=data['user']['email'],
                            user_role=data['user']['user_role'])
                airline = AirlineCompany(id=data['airline']['id'],
                                         name=data['airline']['name'],
                                         country_id=data['airline']['country_id'],
                                         iata=data['airline']['iata'],
                                         user_id=data['airline']['user_id'])
                token = facade.update_airline(airline_id, airline, user)
                response = token

            case Actions.ADD_FLIGHT:
                flight = Flight(id=data['flight']['id'],
                                airline_company_id=data['flight']['airline_company_id'],
                                origin_country_id=data['flight']['origin_country_id'],
                                destination_country_id=data['flight']['destination_country_id'],
                                departure_time=GenericService.compose_datetime(
                                    data['flight']['departure_date'],
                                    data['flight']['departure_hour'],
                                    data['flight']['departure_minute'], '/'),
                                landing_time=GenericService.compose_datetime(
                                    data['flight']['landing_date'],
                                    data['flight']['landing_hour'],
                                    data['flight']['landing_minute'], '/'),
                                price=data['flight']['price'],
                                remaining_tickets=data['flight']['remaining_tickets'],
                                distance=data['flight']['distance'],
                                num_seats=data['flight']['num_seats'])
                new_flight = facade.add_flight(flight)
                response = new_flight

            case Actions.UPDATE_FLIGHT:
                flight_id = data['flight_id']
                flight = Flight(id=data['flight']['id'],
                                airline_company_id=data['flight']['airline_company_id'],
                                origin_country_id=data['flight']['origin_country_id'],
                                destination_country_id=data['flight']['destination_country_id'],
                                departure_time=GenericService.compose_datetime(
                                    data['flight']['departure_date'],
                                    data['flight']['departure_hour'],
                                    data['flight']['departure_minute'], '/'),
                                landing_time=GenericService.compose_datetime(
                                    data['flight']['landing_date'],
                                    data['flight']['landing_hour'],
                                    data['flight']['landing_minute'], '/'),
                                price=data['flight']['price'],
                                remaining_tickets=data['flight']['remaining_tickets'],
                                distance=data['flight']['distance'],
                                num_seats=data['flight']['num_seats'])
                facade.update_flight(flight_id, flight)
                response ={'success': 'OK'}
            case Actions.REMOVE_FLIGHT:
                fligth_id = data['flight_id']
                facade.remove_flight(fligth_id)
                response ={'success': 'OK'}
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

            case Actions.GET_FLIGHT_BY_PARAMS:
                origin_country_id = data['origin_country_id']
                dest_country_id = data['dest_country_id']
                start_date = data['start_date']
                end_date = data['end_date']
                response = facade.get_flights_by_parameters(origin_country_id, dest_country_id, start_date, end_date)

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

            case Actions.GET_CUSTOMER_BY_ID:
                customer_id = data['customer_id']
                response = facade.get_customer_by_id(customer_id)

            case Actions.UPDATE_CUSTOMER:
                customer_id = data['customer_id']
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
                                    image_url=data['customer']['image_url'],
                                    user_id=data['customer']['user_id'])
                token = facade.update_customer(customer_id, customer, user)
                response = token

            case Actions.CHECK_TICKET:
                 ticket = Ticket(
                    flight_id=data['ticket']['flight_id'],
                    customer_id=data['ticket']['customer_id'],
                    position=data['ticket']['position']
                    )
                 flight = facade.get_flight_by_id(ticket.flight_id)
                 ticket.price = flight.price
                 can_order_ticket = facade.check_ticket(ticket)
                 response = can_order_ticket

            case Actions.ADD_TICKET:
                ticket = Ticket(
                    flight_id=data['ticket']['flight_id'],
                    customer_id=data['ticket']['customer_id'],
                    position=data['ticket']['position']
                )
                flight=facade.get_flight_by_id(ticket.flight_id)
                ticket.price =flight.price

                new_ticket = facade.add_ticket(ticket)
                response = new_ticket

            case Actions.REMOVE_TICKET:
                ticket_id = data['ticket_id']
                facade.remove_ticket(ticket_id)
                response = {'success': 'OK'}

            case Actions.GET_TICKETS_BY_CUSTOMER:
                customer_id = data['customer_id']
                response = facade.get_my_tickets(customer_id)

            case Actions.GET_TICKETS_BY_FLIGHT:
                flight_id = data['flight_id']
                response = facade.get_tickets_by_flight(flight_id)
        return response





