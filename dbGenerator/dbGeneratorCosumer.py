import pika
import json
import random
from datetime import datetime, timedelta
from common.entities.db_config import local_session, create_all_entities
from common.entities.db_conifg_procedured import load_db_scripts
from business.facade.DbGeneratorFacade import BdGeneratorFacade
from business.services.testService import TestService
from dataAccess.FlightRepository import FilghtRepository
from common.entities.Country import Country
from common.entities.Administrator import Administrator
from common.entities.User import User
from common.entities.AirlineCompany import AirlineCompany
from common.entities.Customer import Customer
from common.entities.Flight import Flight
from common.entities.Ticket import Ticket
from common.constants.enums import UserRoles, Reason, DbGenerationOpetion
from business.services.genericService import GenericService
from common.exceptions.notValidOrderException import NotValidOrderException
from dbGenerator.consumeParams import ConsumeParams
from dbGenerator.generateErrors import GenerateErrors


class DbGeneratorConsumer:
    QUEUE_NAME = 'FlightSystemData'
    RESPONSE_QUEUE_NAME = 'FlightSysDbUpdateProgress'

    minimum_flight_time = 30  # MIN FLIGHT_TIME = 30 MINUTES
    maximum_flight_time = 1440  # MAX FLIGHT_TIME = 24H
    minutes_start = 1440  # one day ahead
    minutes_end = 216000  # 5 months ahead
    tickets_per_flight = 40

    def __init__(self):
        # DB
        self.repository = FilghtRepository(local_session)
        self._db_generator_facade = BdGeneratorFacade(local_session)
        DbGeneratorConsumer.init_data_base()
        # RABBIT MQ
        self.connection = None
        self.channel = None
        self.response_connection = None
        self.response_channel = None
        self.init_connection()
        self.init_response_connection()
        self.consume_params = None

    def init_connection(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_delete(self.QUEUE_NAME)
        self.channel.queue_declare(queue=self.QUEUE_NAME)

    def init_response_connection(self):
        self.response_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.response_channel = self.response_connection.channel()
        self.response_channel.queue_declare(queue=self.RESPONSE_QUEUE_NAME)

    @staticmethod
    def init_data_base():
        create_all_entities()
        load_db_scripts()

    def replace_data_base(self, is_replace):
        test_service = TestService(local_session, self.repository)
        test_service.restore_database_no_recreate(is_replace)

    def consume_db_generator(self):
        try:
            self.channel.basic_consume(queue=self.QUEUE_NAME, on_message_callback=self.db_generator_callback, auto_ack=True)
            print(' [*] Waiting for messages. To exit press CTRL+C')
            self.channel.start_consuming()
            self.channel.queue_delete(self.QUEUE_NAME)
            self.connection.close()
        except KeyboardInterrupt:
            self.channel.queue_delete(self.QUEUE_NAME)
            self.connection.close()
        except Exception as exp:
            self.channel.queue_delete(self.QUEUE_NAME)
            self.connection.close()
            raise exp

    def db_generator_callback(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            consume_type = message['type']
            # if consume_type == 'customer':
            #     pass
            payload = message['payload']
            self.db_consumer_manager(consume_type, payload)
        except Exception as exc:
            return

    def db_consumer_manager(self, consume_type_id, payload):
        match consume_type_id:
            case 'START':
                self.consume_params = ConsumeParams()
                self.consume_params.db_generation_option = int(payload['db_generation_option'])
                is_replace = self.consume_params.db_generation_option == DbGenerationOpetion.REPLACE
                self.replace_data_base(is_replace)
            case 'country':
                try:
                    self.add_country(payload)
                    self.publish_ok_response(consume_type_id)
                except Exception as ex:
                    gen_exc = GenerateErrors.get_add_country_error(ex)
                    self.publish_error_response(consume_type_id, gen_exc)
            case 'airline_name':
                current_names_count = len(self.consume_params.airlines_names)
                airline_name = {'id': current_names_count, 'name': payload, 'selected': False}
                self.consume_params.airlines_names.append(airline_name)
            case 'admin':
                try:
                    # print(f'{consume_type_id}-{datetime.now()} ')
                    self.add_administrator(payload)
                    self.publish_ok_response(consume_type_id)
                except Exception as ex:
                    gen_exc = GenerateErrors.get_add_administrator(ex)
                    self.publish_error_response(consume_type_id, gen_exc)
            case 'airline':
                # print(f'{consume_type_id}-{datetime.now()} ')
                self.add_airline(payload)
            case 'customer':
                # print(f'{consume_type_id}-{datetime.now()} ')
                self.add_customer(payload)
            case 'COMPLETED':
                self.publish_complete_response()

    def publish_ok_response(self, consume_type):
        ok_response = json.dumps({
            'object_type': consume_type,
            'message_type': 'OK',
            'error_desc': ''
        })
        self.response_channel.basic_publish(exchange='',
                                            routing_key=self.RESPONSE_QUEUE_NAME,
                                            body=ok_response)

    def publish_error_response(self, consume_type, exc):
        root_exc = GenericService.get_root_exception(exc)
        err_response = json.dumps({
            'object_type': consume_type,
            'message_type': 'ERROR',
            'error_desc': str(root_exc)
        })
        self.response_channel.basic_publish(exchange='',
                                            routing_key=self.RESPONSE_QUEUE_NAME,
                                            body=err_response)

    def publish_complete_response(self):
        complete_response = json.dumps({
            'object_type': 'COMPLETED',
            'message_type': 'COMPLETED',
            'error_desc': ''
        })
        self.response_channel.basic_publish(exchange='',
                                            routing_key=self.RESPONSE_QUEUE_NAME,
                                            body=complete_response)

    def init_countries(self):
        is_req_init = self.consume_params.count_countries_names == 0
        if is_req_init:
            countries = self._db_generator_facade.get_all_countries()
            self.consume_params.count_countries_names = len(countries)

    def init_availiable_flights(self):
        is_req_flights = self.consume_params.avail_flights is None
        if is_req_flights:
            self.consume_params.avail_flights = [flight for flight in self._db_generator_facade.get_all_flights()
            if flight.remaining_tickets > 0 and flight.departure_time > self.consume_params.start_time]

    def add_country(self, country_name):
        country = Country(id=None, name=country_name[:Country.NAME_MAX])
        self._db_generator_facade.add_country(country)

    def add_administrator(self, payload):
        admin_user = User(
            id=None,
            username=payload['username'][:User.USERNAME_MAX],
            password=payload['password'][:User.PASSWORD_MAX],
            email=payload['email'][:User.EMAIL_MAX],
            user_role=UserRoles.ADMINISTATOR
        )
        admin = Administrator(
            id=None,
            first_name=payload['first_name'][:Administrator.FIRST_NAME_MAX],
            last_name=payload['last_name'][:Administrator.LAST_NAME_MAX],
            user_id=None
        )
        self._db_generator_facade.add_administrator(admin, admin_user)

    def add_airline(self, payload):
        # COUNTRIES BANK
        self.init_countries()
        # AIRLINEs
        airline_user = User(
            id=None,
            username=payload['username'][:User.USERNAME_MAX],
            password=payload['password'][:User.PASSWORD_MAX],
            email=payload['email'][:User.EMAIL_MAX],
            user_role=UserRoles.AIRLINE
        )
        airline_name_entry = None
        while True:
            airline_name_index = random.randint(1, len(self.consume_params.airlines_names)) - 1
            airline_name_entry = self.consume_params.airlines_names[airline_name_index]
            if not airline_name_entry['selected']:
                break
        airline_country_id = random.randint(1, self.consume_params.count_countries_names)
        airline = AirlineCompany(
            id=None,
            name=airline_name_entry['name'][:AirlineCompany.MAX_NAME],
            country_id=airline_country_id,
            user_id=None
        )
        try:
            self._db_generator_facade.add_airline(airline, airline_user)
            self.publish_ok_response('airline')
        except Exception as ex:
            gen_exc = GenerateErrors.get_add_airline_error(ex)
            self.publish_error_response('airline', gen_exc)
            self.add_error_airline_flights(payload['flights_per_airline'], gen_exc)
            return
        airline_name_entry['selected'] = True
        self.add_airline_flights(airline.id, payload['flights_per_airline'])
        # AIRLINE FLIGHTS

    def add_airline_flights(self, airline_id, flights_per_airline):
        flights_per_airline = int(flights_per_airline)
        for flight_index in range(flights_per_airline):
            try:
                flight = DbGeneratorConsumer.create_flight(airline_id, self.consume_params.count_countries_names)
                self._db_generator_facade.add_flight(flight)
                self.publish_ok_response('flight')
            except Exception as exc:
                gen_exc = GenerateErrors.get_add_flight_error(exc)
                self.publish_error_response('flight', gen_exc)

    def add_error_airline_flights(self, flights_per_airline_param, exc):
        flights_per_airline = int(flights_per_airline_param)
        for flight_index in range(flights_per_airline):
            self.publish_error_response('flight', exc)

    def add_customer(self, payload):
        self.init_availiable_flights()
        customer_user = User(
            id=None,
            username=payload['username'][:User.USERNAME_MAX],
            password=payload['password'][:User.PASSWORD_MAX],
            email=payload['email'][:User.EMAIL_MAX],
            user_role=UserRoles.CUSTOMER
        )
        customer = Customer(
            id=None,
            first_name=payload['first_name'][:Customer.MAX_FIRST_NAME],
            last_name=payload['last_name'][:Customer.MAX_LAST_NAME],
            address=payload['address'][:Customer.MAX_ADDRESS],
            phone_number=payload['phone_number'][:Customer.MAX_PHONE],
            credit_card_number=payload['credit_card_number'][:Customer.MAX_CREDIT_CARD],
            user_id=None
        )
        try:
            self._db_generator_facade.add_customer(customer, customer_user)
            self.publish_ok_response('customer')
        except Exception as exc:
            gen_exc = GenerateErrors.get_add_customer_error(exc)
            self.publish_error_response('customer', gen_exc)
            self.add_error_tickets(payload['tickets_per_customer'], gen_exc)
            return
        self.add_customer_tickets(customer.id, payload['tickets_per_customer'])

    # CUSTOMER TICKETS
    def add_customer_tickets(self, customer_id,  tickets_per_customer_param):
        tickets_per_customer = int(tickets_per_customer_param)
        # ALL AVALIABLE 4 CUSTOMER FLIGHTS:
        avail_flight_count = len(self.consume_params.avail_flights)
        cust_not_valid_flights = []
        for ticket_index in range(tickets_per_customer):
            try:
                while True:
                    no_customer_tickets = len(cust_not_valid_flights) == avail_flight_count
                    if no_customer_tickets:
                        exc = NotValidOrderException('ticket', Reason.FLIGHT_SOLD_OUT)
                        gen_exc = GenerateErrors.get_add_ticket_error(exc)
                        self.publish_error_response('ticket', gen_exc)
                        break
                    # TICKET
                    ticket = DbGeneratorConsumer.create_ticket(customer_id,
                                                               self.consume_params.avail_flights,
                                                               cust_not_valid_flights)
                    ticket_result = self._db_generator_facade.add_ticket(ticket)
                    if ticket_result:
                        # TICKET OK
                        cust_not_valid_flights.append(ticket.flight_id)
                        self.publish_ok_response('ticket')
                        break
                    # TICKET REJECTED
                    cust_not_valid_flights.append(ticket.flight_id)
            except Exception as exc:
                self.publish_error_response('ticket', exc)

    def add_error_tickets(self, tickets_per_customer_param, exc):
        tickets_per_customer = int(tickets_per_customer_param)
        for ticket_index in range(tickets_per_customer):
            self.publish_error_response('ticket', exc)

    @staticmethod
    def create_flight(airline_company_id, count_countries):
        origin_country_id = random.randint(1, count_countries)
        destination_country_id = None
        while True:
            destination_country_id = random.randint(1, count_countries)
            if destination_country_id != origin_country_id:
                break
        current_time = datetime.now()
        # RANDOM TIMES
        departure_rnd_minutes = random.randint(DbGeneratorConsumer.minutes_start,
                                               DbGeneratorConsumer.minutes_end)
        departure_time = current_time + timedelta(minutes=departure_rnd_minutes)
        landing_rnd_minutes = random.randint(DbGeneratorConsumer.minimum_flight_time,
                                             DbGeneratorConsumer.maximum_flight_time)
        landing_time = departure_time + timedelta(minutes=landing_rnd_minutes)
        remaining_tickets = DbGeneratorConsumer.tickets_per_flight
        # ******
        flight = Flight(id=None,
                        airline_company_id=airline_company_id,
                        origin_country_id=origin_country_id,
                        destination_country_id=destination_country_id,
                        departure_time=departure_time,
                        landing_time=landing_time,
                        remaining_tickets=remaining_tickets
                        )
        return flight

    @staticmethod
    def create_ticket(cust_id, avail_flights, customer_flights):
        filter_flights = [flight.id for flight in avail_flights if flight.id not in customer_flights]
        flight_index = random.randint(1, len(filter_flights)) - 1
        flight_id = filter_flights[flight_index]
        customer_id = cust_id
        ticket = Ticket(
            id=None,
            flight_id=flight_id,
            customer_id=customer_id
        )
        return ticket


def main():
    consumer = DbGeneratorConsumer()
    consumer.consume_db_generator()


if __name__ == '__main__':
    main()
