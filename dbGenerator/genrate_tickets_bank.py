from dataAccess.FlightRepository import FilghtRepository
from common.entities.db_config import local_session, create_all_entities
from common.entities.db_conifg_procedured import load_db_scripts
from common.entities.Customer import Customer
from common.entities.Flight import Flight
from common.entities.Ticket import Ticket
import random
import math
import datetime

from sqlalchemy import func

ITERATIONS = 5000

seats_models = [
    {'seats' :  120, 'rows': 20, 'cols': 6},
    {'seats' :  180, 'rows': 30, 'cols': 6},
    {'seats' :  200, 'rows': 25, 'cols': 8},
    {'seats' :  240, 'rows': 24, 'cols': 10},
    {'seats' :  300, 'rows': 30, 'cols': 10}
]

class generate_tickets_bank:
    def __init__(self):
        create_all_entities()
        load_db_scripts()
        self.repository = FilghtRepository(local_session)

    def generate(self):
        customers = self.repository.get_all(Customer)
        customer_count = len(customers)

        #flights
        # start_date = datetime.datetime(2022, 9, 1)
        # end_date = datetime.datetime(2022, 9, 30)
        # flight_condition = (lambda query: query.filter(Flight.departure_time >=start_date,
        #                                                Flight.departure_time <=end_date))
        flights = self.repository.get_all(Flight)
        flights_count = len(flights)

        for i in range(5000):
            # get random customer
            customer_index = math.floor(random.random() * customer_count)
            customer = customers[customer_index]

            # get random flight
            # primary key (flight, customer) mustn't be violated
            # flight only with remaining_tickets >0
            # no customer cross flights
            while True:
                flight_index = math.floor(random.random() * flights_count)
                flight = flights[flight_index]
                db_flight = self.repository.get_by_id(Flight, flight.id)
                if db_flight.remaining_tickets == 0:
                    continue
                flight_customer_condition = (lambda query: query.filter(Ticket.flight_id == db_flight.id,
                                                                        Ticket.customer_id == customer.id))
                flight_customer_tickets = self.repository.get_all_by_condition(Ticket, flight_customer_condition)
                if len(flight_customer_tickets) >0:
                    continue
                db_cross_flights = self.repository.get_customer_cross_flight(customer.id, db_flight.id)
                if len(db_cross_flights) > 0:
                    continue
                break
            # flight matched
            model = self.get_seats_model(db_flight.num_seats)

            # get position
            while True:
                row_count = model['rows']
                columns_count = model['cols']
                random_row = math.floor(random.random() * row_count)
                random_col = math.floor(random.random() * columns_count)
                format_position = f'{random_row + 1}-{random_col + 1}'

                ticket_pos_condition = (lambda query: query.filter(Ticket.flight_id == db_flight.id,
                                                                   Ticket.position == format_position))
                match_position_ticket = self.repository.get_all_by_condition(Ticket, ticket_pos_condition)
                is_match_ticket = len(match_position_ticket) == 0
                if is_match_ticket:
                    break

            # postion selected
            # insert new ticket
            ticket_price = db_flight.price
            new_ticket = Ticket(flight_id=db_flight.id,
                               customer_id=customer.id,
                               position=format_position,
                               price=ticket_price)

            remaining_tickets = db_flight.remaining_tickets - 1
            self.repository.add_ticket(new_ticket, remaining_tickets)

            print(f'Inseted Num {i}')

    def get_seats_model(self, num_seats):
        for model in seats_models:
            if model['seats'] == num_seats:
                return model
        return None

bank = generate_tickets_bank()
bank.generate()

print('Done! ')