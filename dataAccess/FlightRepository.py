import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.orm.query
import sqlalchemy.ext.declarative
from sqlalchemy import asc, text, desc, delete, update
from sqlalchemy.orm import join
from business.services.loggingService import FlightsLogger
from common.entities.Customer import Customer
from common.entities.Ticket import Ticket
from common.entities.Flight import Flight
from common.entities.User import User
from common.entities.AirlineCompany import AirlineCompany
from common.entities.Administrator import Administrator
from sqlalchemy import text
from datetime import datetime, timedelta
from common.entities.Country import Country
import logging


class FilghtRepository:
    def __init__(self, local_session):
        self.local_session = local_session
        self.logger = FlightsLogger.get_instance().Logger

    def execute_script(self, text_command):
        try:
            self.local_session.execute(text_command)
            self.logger.log(logging.INFO, f'execute_script')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'execute_script: {str(ex)}')
            raise ex

    # reset_table_auto_incerement
    def reset_table_auto_incerement(self, table_class):
        try:
            self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')
            # SUCCEDED
            self.logger.log(logging.INFO, f'reset_table_auto_incerement: {table_class.__tablename__}')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'reset_table_auto_incerement: {str(ex)}')
            raise ex

    # get_by_id
    def get_by_id(self, table_class, entry_id):
        try:
            entry = self.local_session.query(table_class).get(entry_id)
            # SUCCEDED
            # self.logger.log(logging.INFO, f'get_by_id: {str(entry)}')
            return entry
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_by_id: {str(ex)}')
            raise ex

    # get all
    def get_all(self, table_class):
        try:
            entries = self.local_session.query(table_class).all()
            # SUCCEDED
            # self.logger.log(logging.INFO, f'get_all: {str(entries)}')
            return entries
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_all: {str(ex)}')
            raise ex

    # get all by condition
    def get_all_by_condition(self, table_class, condition):
        try:
            query = self.local_session.query(table_class)
            entries = filter(condition, query).all()
            # SECCEDED
            # self.logger.log(logging.INFO, f'get_all_by_condition: {str(entries)}')
            return entries
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_all_by_condition: {str(ex)}')
            raise ex

    # get_all_by_condition
    def get_all_by_condition(self, table_class, condition):
        try:
            query = self.local_session.query(table_class)
            entries = condition(query).all()
            # SECCEDED
            # self.logger.log(logging.INFO, f'get_all_by_condition: {str(entries)}')
            return entries
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_all_by_condition: {str(ex)}')
            raise ex

    # get all limit
    def get_all_limit(self, table_class, limit_num):
        try:
            entries = self.local_session.query(table_class).limit(limit_num).all()
            self.logger.log(logging.INFO, f'get_all_limit: {str(entries)}')
            # SECCEDED
            return entries
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_all_limit: {str(ex)}')
            raise ex

    # get all order by
    def get_all_order_by(self, table_class, column_name, direction=asc):
        try:
            entries = self.local_session.query(table_class).order_by(direction(column_name)).all()
            # SECCEDED
            self.logger.log(logging.INFO, f'get_all_order_by: {str(entries)}')
            return entries
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_all_order_by: {str(ex)}')
            raise ex

    # add
    def add(self, entry):
        try:
            self.local_session.add(entry)
            self.local_session.flush()
            self.local_session.commit()
            # SECCEDED
            self.logger.log(logging.INFO, f'add: {str(entry)}')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'add: {str(ex)}')
            raise ex

    # add all
    def add_all(self, entries):
        try:
            self.local_session.add_all(entries)
            self.local_session.commit()
            # self.local_session.commit()
            # SECCEDED
            self.logger.log(logging.INFO, f'add_all: {str(entries)}')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'add_all: {str(ex)}')
            raise ex

    # update
    def update(self, table_class, id_column_name, entry_id, data):
        try:
            entry = self.local_session.query(table_class).filter(getattr(table_class, id_column_name) == entry_id)
            entry.update(data)
            self.local_session.commit()
            # SECCEDED
            self.logger.log(logging.INFO, f'update: {table_class}, {entry_id}, {str(data)}')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'update: {str(ex)}')
            raise ex

    # update_all_by_condition
    def update_all_by_condition(self, table_class, condition, data):
        try:
            query = self.local_session.query(table_class)
            entries = condition(query)
            entries.update(data)
            self.local_session.commit()
            # SECCEDED
            self.logger.log(logging.INFO, f'update_all_by_condition: {table_class}, {entries}, {str(data)}')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'update_all_by_condition: {str(ex)}')
            raise ex

    # delete
    def remove(self, table_class, id_column_name, entry_id):
        try:
            entry = self.local_session.query(table_class).filter(getattr(table_class, id_column_name) == entry_id)
            entry.delete(synchronize_session=False)
            self.local_session.commit()
            # SECCEDED
            self.logger.log(logging.INFO, f'remove: {entry}')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'remove: {str(ex)}')
            raise ex

    # delete_all_by_condition
    def remove_all_by_condition(self, table_class, condition):
        try:
            query = self.local_session.query(table_class)
            entries = condition(query)
            entries.delete(synchronize_session=False)
            self.local_session.commit()
            # SECCEDED
            self.logger.log(logging.INFO, f'delete_all_by_condition: {entries}')
        except Exception as ex:
            self.logger.log(logging.ERROR, f'remove_all_by_condition: {str(ex)}')
            raise ex

    def commit(self):
        self.local_session.commit()

    def add_customer(self, customer, user):
        try:
            self.local_session.add(user)
            self.local_session.flush()
            customer.user_id = user.id
            self.local_session.add(customer)
            self.local_session.commit()
            self.logger.log(logging.INFO, f'add_customer')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'add_customer: {str(ex)}')
            raise ex

    def add_airline(self, airline, user):
        try:
            self.local_session.add(user)
            self.local_session.flush()
            airline.user_id = user.id
            self.local_session.add(airline)
            self.local_session.commit()
            self.logger.log(logging.INFO, f'add_airline')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'add_airline: {str(ex)}')
            raise ex

    def add_administrator(self, administrator, user):
        try:
            self.local_session.add(user)
            self.local_session.flush()
            administrator.user_id = user.id
            self.local_session.add(administrator)
            self.local_session.commit()
            self.logger.log(logging.INFO, f'add_administrator')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'add_administrator: {str(ex)}')
            raise ex

    # custom functions ==> not generic
    def remove_customer(self, customer_id, customer_user_id):
        # customer tickets
        try:
            customer_tickets_cond = (lambda query: query.filter(Ticket.customer_id == customer_id))
            customer_tickets_query = self.local_session.query(Ticket)
            tickets_entries = customer_tickets_cond(customer_tickets_query)
            tickets_entries.delete(synchronize_session=False)
            # customer
            cust_entry = self.local_session.query(Customer).filter(getattr(Customer, 'id') == customer_id)
            cust_entry.delete(synchronize_session=False)
            user_entry = self.local_session.query(User).filter(getattr(User, 'id') == customer_user_id)
            user_entry.delete(synchronize_session=False)
            self.local_session.commit()
            self.logger.log(logging.INFO, f'remove_customer: {customer_id}')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'remove_all_by_condition: {str(ex)}')
            raise ex

    def remove_airline(self, airline_id):
        # airline flights
        try:
            stmt = text('CALL remove_airline(:_airline_company_id)') \
                .bindparams(_airline_company_id=airline_id)
            self.local_session.execute(stmt)
            self.local_session.commit();
            self.logger.log(logging.INFO, f'remove_airline')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'remove_airline: {str(ex)}')
            raise ex

    def remove_administrator(self, administrator_id):
        # airline flights
        try:
            stmt = text('CALL remove_administrator(:_administrator_id)') \
                .bindparams(_administrator_id=administrator_id)
            self.local_session.execute(stmt)
            self.local_session.commit()
            self.logger.log(logging.INFO, f'remove_administrator')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'remove_administrator: {str(ex)}')
            raise ex

    def add_ticket(self, ticket: Ticket, remaining_tickets):
        try:
            self.local_session.add(ticket)
            updated_data_filter = {'remaining_tickets': remaining_tickets}
            self.update(Flight, 'id', ticket.flight_id, updated_data_filter)
            self.local_session.commit()
            # self.logger.log(logging.INFO, f'add_ticket: {ticket}')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'remove_all_by_condition: {str(ex)}')
            raise ex

    def remove_flight(self, fligth_id):
        try:
            fligth_tickets = self.local_session.query(Ticket).filter(getattr(Ticket, 'flight_id') == fligth_id)
            fligth_tickets.delete(synchronize_session=False)
            flight = self.local_session.query(Flight).filter(getattr(Flight, 'id') == fligth_id)
            flight.delete(synchronize_session=False)
            self.local_session.commit()
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'remove_flight: {str(ex)}')
            raise ex

    def remove_ticket(self, ticket_id, flight_id, reamining_tickets):
        try:
            ticket_entry = self.local_session.query(Ticket).filter(getattr(Ticket, 'id') == ticket_id)
            ticket_entry.delete(synchronize_session=False)
            updated_data_filter = {'remaining_tickets': reamining_tickets}
            flight_entry = self.local_session.query(Flight).filter(getattr(Flight, 'id') == flight_id)
            flight_entry.update(updated_data_filter)
            self.local_session.commit()
            self.logger.log(logging.INFO, f'remove_ticket: {ticket_id}')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'remove_all_by_condition: {str(ex)}')
            raise ex

    def update_customer(self, user_id, user, customer_id,  customer):
        try:
            user_updated_data = {
                'username': user.username,
                'password': user.password,
                'email': user.email
            }
            customer_updated_data = {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'address': customer.address,
                'phone_number': customer.phone_number,
                'credit_card_number': customer.credit_card_number,
                'image_url': customer.image_url,
            }
            user_entry = self.local_session.query(User).filter(getattr(User, "id") == user_id)
            user_entry.update(user_updated_data)
            cust_entry = self.local_session.query(Customer).filter(getattr(Customer, "id") == customer_id)
            cust_entry.update(customer_updated_data)
            self.local_session.commit()
            self.logger.log(logging.INFO, f'update_customer: {customer_id}')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'update_customer: {str(ex)}')
            raise ex

    def update_airline(self, user_id, user, airline_id,  airline):
        try:
            user_updated_data = {
                'username': user.username,
                'password': user.password,
                'email': user.email,
            }
            airline_updated_data = {
                'name': airline.name,
                'country_id': airline.country_id,
                'iata': airline.iata
            }
            user_entry = self.local_session.query(User).filter(getattr(User, "id") == user_id)
            user_entry.update(user_updated_data)

            airline_entry = self.local_session.query(AirlineCompany).filter(getattr(AirlineCompany, "id") == airline_id)
            airline_entry.update(airline_updated_data)
            self.local_session.commit()
            self.logger.log(logging.INFO, f'update_airline: {airline_id}')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'update_airline: {str(ex)}')
            raise ex

    def update_administrator(self, user_id, user, administrator_id,  administrator):
        try:
            user_updated_data = {
                'username': user.username,
                'password': user.password,
                'email': user.email
            }
            admin_updated_data = {
                'first_name': administrator.first_name,
                'last_name': administrator.last_name,
                'image_url': administrator.image_url
            }
            user_entry = self.local_session.query(User).filter(getattr(User, "id") == user_id)
            user_entry.update(user_updated_data)

            admin_entry = self.local_session.query(Administrator).filter(getattr(Administrator, "id") == administrator_id)
            admin_entry.update(admin_updated_data)
            self.local_session.commit()
            self.logger.log(logging.INFO, f'update_administrator: {administrator_id}')
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'update_administrator: {str(ex)}')
            raise ex

    def get_customer_cross_flight(self, customer_id, new_flight_id):
        try:
            stmt = text('select * from get_overlapped_filghts(:_customer_id, :_new_flight_id)') \
                .bindparams(_customer_id=customer_id, _new_flight_id=new_flight_id)
            flight_entries = self.local_session.execute(stmt).all()
            # self.logger.log(logging.INFO, f'get_customer_cross_flight: {flight_entries}')
            return flight_entries
        except Exception as ex:
            self.logger.log(logging.ERROR, f'remove_all_by_condition: {str(ex)}')
            raise ex

    # added function (alchemy)
    def get_airlines_by_country(self, country_id):
        try:
            airlines = self.local_session.query(AirlineCompany).filter(AirlineCompany.country_id == country_id).all()
            self.logger.log(logging.INFO, f'get_airlines_by_country: {airlines}')
            return airlines
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_airlines_by_country: {str(ex)}')
            raise ex

    def get_flights_by_origin_country_id(self, country_id):
        try:
            fligths = self.local_session.query(Flight).filter(Flight.origin_country_id == country_id).all()
            self.logger.log(logging.INFO, f'get_flights_by_origin_country_id: {fligths}')
            return fligths
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_flights_by_origin_country_id: {str(ex)}')
            raise ex

    def get_flights_by_dest_country_id(self, country_id):
        try:
            fligths = self.local_session.query(Flight).filter(Flight.destination_country_id == country_id).all()
            self.logger.log(logging.INFO, f'get_flights_by_dest_country_id: {fligths}')
            return fligths
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_flights_by_dest_country_id: {str(ex)}')
            raise ex

    def get_flights_by_depaerture_date(self, daparture_date):
        try:
            start_time = daparture_date
            end_time = start_time + timedelta(days=1)
            flights = self.local_session.query(Flight).filter(Flight.departure_time >= start_time,
                                                          Flight.departure_time < end_time).all()
            self.logger.log(logging.INFO, f'get_flights_by_depaerture_date: {flights}')
            return flights
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_flights_by_depaerture_date: {str(ex)}')
            raise ex

    def get_flights_by_landing_date(self, landing_date):
        try:
            start_time = landing_date
            end_time = start_time + timedelta(days=1)
            flights = self.local_session.query(Flight).filter(Flight.landing_time >= start_time,
                                                          Flight.landing_time < end_time).all()
            self.logger.log(logging.INFO, f'get_flights_by_landing_date: {flights}')
            return flights
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_flights_by_landing_date: {str(ex)}')
            raise ex

    def get_flights_by_customer(self, customer_id):
        try:
            customer_flights = self.local_session.query(Customer) \
                .join(Ticket, Customer.id == Ticket.customer_id) \
                .join(Flight, Ticket.flight_id == Flight.id) \
                .join(Country, Flight.destination_country_id == Country.id) \
                .join(AirlineCompany, Flight.airline_company_id == AirlineCompany.id) \
                .filter(Customer.id == customer_id) \
                .with_entities(Flight.id, AirlineCompany.name, AirlineCompany.iata, Country.name, Flight.departure_time, Flight.landing_time).all()
            self.logger.log(logging.INFO, f'get_flights_by_customer: {customer_flights}')
            return customer_flights
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_flights_by_customer: {str(ex)}')
            raise ex

    def get_customer_by_username(self, username):
        try:
            stmt = text('select * from get_cusotmer_by_username(:_username)') \
                .bindparams(_username=username)
            customer = self.local_session.execute(stmt).first()
            self.logger.log(logging.INFO, f'get_customer_by_username: {customer}')
            return customer
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_customer_by_username: {str(ex)}')
            raise ex

    def get_airline_by_username(self, username):
        try:
            stmt = text('select * from get_airline_comp_by_username(:_username)') \
                .bindparams(_username=username)
            airline = self.local_session.execute(stmt).first()
            self.logger.log(logging.INFO, f'get_airline_by_username: {airline}')
            return airline
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_airline_by_username: {str(ex)}')
            raise ex

    def get_customer_by_id(self, customer_id):
        try:
            customers = self.local_session.query(Customer) \
            .join(User, Customer.user_id == User.id) \
            .filter(Customer.id == customer_id) \
            .with_entities(User.username, User.password, User.email, Customer.first_name, \
                           Customer.last_name, Customer.address, Customer.phone_number, \
                           Customer.credit_card_number).all()
            if len(customers) == 0:
                return None
            customer = customers[0]
            return customer
        except Exception as ex:
            self.logger.log(logging.ERROR, f'get_customer_by_id: {str(ex)}')
            raise ex

    def get_administrator_by_username(self, username):
        try:
            stmt = text('select * from get_administrator_by_username(:_username)') \
                .bindparams(_username=username)
            administrator = self.local_session.execute(stmt).first()
            self.logger.log(logging.INFO, f'get_administrator_by_username: {administrator}')
            return administrator
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_administrator_by_username: {str(ex)}')
            raise ex

    def get_user_by_username(self, username):
        try:
            stmt = text('select * from get_user_by_username(:_username)') \
                .bindparams(_username=username)
            user = self.local_session.execute(stmt).first()
            self.logger.log(logging.INFO, f'get_user_by_username: {user}')
            return user
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_user_by_username: {str(ex)}')
            raise ex

    def get_flights_by_parameters(self, origin_country_id, dest_country_id, start_date, end_date):
        try:
            stmt = text(f'select * from get_flights_by_parameters(:_origin_counry_id, '
                        f':_detination_country_id, :_start_date, :_end_date)') \
                .bindparams(_origin_counry_id=origin_country_id, _detination_country_id=dest_country_id,
                            _start_date=start_date, _end_date=end_date)
            results = self.local_session.execute(stmt).all()
            flights = [{'flight_id': res[0],
                        'airline_company_id': res[1],
                        'airline_company_name': res[2],
                        'airline_iata': res[3],
                        'origin_country_id': res[4],
                        'origin_country_name': res[5],
                        'origin_country_airport_abbr': res[6],
                        'destination_country_id': res[7],
                        'dest_country_name': res[8],
                        'dest_country_airport_abbr': res[9],
                        'departure_time': res[10],
                        'landing_time': res[11],
                        'price': float(res[12]),
                        'remaining_tickets': res[13],
                        'num_seats': res[14]
                        } for res in results]
            # self.logger.log(logging.INFO, f'get_flights_by_parameters: {flights}')
            return flights
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_flights_by_parameters: {str(ex)}')
            raise ex

    def get_customers_bussines_data(self, search):
        try:
            stmt = text(f'select * from get_customers_bussines_data(:_search)').bindparams(_search=search)
            results = self.local_session.execute(stmt).all()
            customers = [{'id': res[0],
                          'first_name': res[1],
                          'last_name': res[2],
                          'image_url': res[3],
                          'last_activity_date': res[4],
                          'email': res[5],
                          'address': res[6],
                          'phone_number': res[7],
                          'num_tickets': res[8],
                          'total_purchases': float(res[9])
                        } for res in results]
            # self.logger.log(logging.INFO, f'get_customers_bussines_data: {customers}')
            return customers
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_customers_bussines_data: {str(ex)}')
            raise ex

    def get_airlines_bussines_data(self, search):
        try:
            stmt = text(f'select * from get_airlines_bussines_data(:_search)').bindparams(_search=search)
            results = self.local_session.execute(stmt).all()
            airlines = [{'id': res[0],
                          'country_id': res[1],
                          'name': res[2],
                          'email': res[3],
                          'iata': res[4],
                          'last_activity_date': res[5],
                          'num_flights': res[6],
                          'sum_sales': res[7]
                         } for res in results]
            # self.logger.log(logging.INFO, f'get_airlines_bussines_data: {airlines}')
            return airlines
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_airlines_bussines_data: {str(ex)}')
            raise ex

    def get_flights_by_airline_id(self, airline_id):
        try:
            stmt = text('select * from get_flights_by_airline_id(:_airline_id)') \
                .bindparams(_airline_id=airline_id)
            results = self.local_session.execute(stmt).all()
            flights = [{'flight_id': res[0],
                        'airline_company_id': res[1],
                        'airline_company_name': res[2],
                        'airline_iata': res[3],
                        'origin_country_id': res[4],
                        'origin_country_name': res[5],
                        'origin_country_airport_abbr': res[6],
                        'destination_country_id': res[7],
                        'dest_country_name': res[8],
                        'dest_country_airport_abbr': res[9],
                        'departure_time': res[10],
                        'landing_time': res[11],
                        'price': float(res[12]),
                        'num_seats': res[13],
                        'distance': res[14],
                        'remaining_tickets': res[15],
                        'revenues': res[16]
                        } for res in results]
           #  self.logger.log(logging.INFO, f'get_flights_by_airline_id: {flights}')
            return flights
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_flights_by_airline_id: {str(ex)}')
            raise ex

    def get_departure_flights(self, country_id):
        try:
            stmt = text('select * from get_departure_flights(:_country_id)') \
                .bindparams(_country_id=country_id)
            flights = self.local_session.execute(stmt).all()
            self.logger.log(logging.INFO, f'get_departure_flights: {flights}')
            return flights
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_departure_flights: {str(ex)}')
            raise ex

    def get_arrival_flights(self, country_id):
        try:
            stmt = text('select * from get_arrival_flights(:_country_id)') \
                .bindparams(_country_id=country_id)
            flights = self.local_session.execute(stmt).all()
            self.logger.log(logging.INFO, f'get_arrival_flights: {flights}')
            return flights
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_arrival_flights: {str(ex)}')
            raise ex

    def get_tickets_by_customer(self, customer_id):
        try:
            stmt = text('select * from get_tickets_by_customer(:_customer_id)') \
                .bindparams(_customer_id=customer_id)
            results = self.local_session.execute(stmt).all()
            tickets = [{'ticket_id': res[0],
                        'flight_id': res[1],
                        'first_name': res[2],
                        'last_name': res[3],
                        'origin_country_name': res[4],
                        'origin_country_airport_abbr': res[5],
                        'destination_country_name': res[6],
                        'dest_country_airport_abbr': res[7],
                        'airline_company_id': res[8],
                        'airline_company_name': res[9],
                        'airline_iata': res[10],
                        'departure_time': res[11],
                        'landing_time': res[12],
                        'seat': res[13],
                        'price': res[14]
                        } for res in results]
            # self.logger.log(logging.INFO, f'get_flights_by_airline_id: {tickets}')
            return tickets
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_flights_by_airline_id: {str(ex)}')
            raise ex

    def get_count_flights(self, start_date, end_date, destination_country_id):
        try:
            stmt = text('select * from get_count_flights(:_start_date, :_end_date, :_destination_country_id)') \
                .bindparams(_start_date=start_date, _end_date=end_date, _destination_country_id=destination_country_id)
            results = self.local_session.execute(stmt).all()
            count_flights = [{'country_id': res[0],
                              'country_name': res[1],
                              'count_flights': res[2]
                        } for res in results]
            # self.logger.log(logging.INFO, f'get_count_flights: {count_flights}')
            return count_flights
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_count_flights: {str(ex)}')
            raise ex

    def get_purchases_by_customers(self, start_date, end_date, destination_country_id):
        try:
            stmt = text('select * from get_purchases_by_customers(:_start_date, :_end_date, :_destination_country_id)') \
                .bindparams(_start_date=start_date, _end_date=end_date, _destination_country_id=destination_country_id)
            results = self.local_session.execute(stmt).all()
            purchases = [{'customer_id': res[0],
                          'customer_name': res[1],
                          'count_tickets': res[2],
                          'sum_purchases': res[3]
                        } for res in results]
            # self.logger.log(logging.INFO, f'get_purchases_by_customers: {purchases}')
            return purchases
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_purchases_by_customers: {str(ex)}')
            raise ex

    def get_sales_by_airlines(self, start_date, end_date, destination_country_id):
        try:
            stmt = text('select * from get_sales_by_airlines(:_start_date, :_end_date, :_destination_country_id)') \
                .bindparams(_start_date=start_date, _end_date=end_date, _destination_country_id=destination_country_id)
            results = self.local_session.execute(stmt).all()
            airlines_sales = [{'airline_id': res[0],
                               'airline_name': res[1],
                               'count_tickets': res[2],
                               'sum_sales': res[3]
                        } for res in results]
            # self.logger.log(logging.INFO, f'get_sales_by_airlines: {airlines_sales}')
            return airlines_sales
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_sales_by_airlines: {str(ex)}')
            raise ex

    def get_daily_sales_data(self, start_date, end_date, destination_country_id):
        try:
            stmt = text('select * from get_daily_sales_data(:_start_date, :_end_date, :_destination_country_id)') \
                .bindparams(_start_date=start_date, _end_date=end_date, _destination_country_id=destination_country_id)
            results = self.local_session.execute(stmt).all()
            daily_sales = [{'result_date': res[0],
                            'result_sales': res[1]
                        } for res in results]
            # self.logger.log(logging.INFO, f'get_daily_sales_data: {daily_sales}')
            return daily_sales
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_daily_sales_data: {str(ex)}')
            raise ex

    def get_capacities_util(self, start_date, end_date, destination_country_id):
        try:
            stmt = text('select * from get_capacities_util(:_start_date, :_end_date, :_destination_country_id)') \
                .bindparams(_start_date=start_date, _end_date=end_date, _destination_country_id=destination_country_id)
            results = self.local_session.execute(stmt).all()
            utils = [{'num_seats': res[0],
                          'remaining_tickets': res[1],
                          'sold_tickets': res[2]
                        } for res in results]
            # self.logger.log(logging.INFO, f'get_purchases_by_customers: {utils}')
            return utils
        except Exception as ex:
            self.local_session.rollback()
            self.logger.log(logging.ERROR, f'get_capacities_util: {str(ex)}')
            raise ex

    def get_customers_by_params(self, search):
        try:
            stmt = text('select * from get_customers_by_params(:_search)') \
            .bindparams(_search=search)
            results = self.local_session.execute(stmt).all()
            customers = [Customer(
                    id=res[0],
                    first_name=res[1],
                    last_name=res[2],
                    address=res[3],
                    phone_number=res[4],
                    credit_card_number=res[5],
                    user_id=res[6],
                    image_url=res[7]
                    ) for res in results]
            return customers

        except Exception as ex:
             self.local_session.rollback()
             self.logger.log(logging.ERROR, f'get_customers_by_params: {str(ex)}')
             raise ex

    def get_administrators_by_params(self, search):
        try:
            stmt = text('select * from get_administrators_by_params(:_search)') \
            .bindparams(_search=search)
            results = self.local_session.execute(stmt).all()
            administrators = [{'id': res[0],
                               'first_name': res[1],
                               'last_name': res[2],
                               'email': res[3],
                               'image_url': res[4]
                        } for res in results]
            return administrators
        except Exception as ex:
             self.local_session.rollback()
             self.logger.log(logging.ERROR, f'get_administrators_by_params: {str(ex)}')
             raise ex

