from common.entities.Flight import Flight
from common.entities.Ticket import Ticket
from common.exceptions.notValidOrderException import NotValidOrderException
from datetime import datetime
from common.constants.enums import Reason, Field, Actions, Entity
from common.exceptions.notFoundException import NotFoundException


class OrdersService:
    def __init__(self, local_session, repository):
        self._repository = repository

    def get_flight_by_id(self, fligth_id):
        flight = self._repository.get_by_id(Flight, fligth_id)
        return flight

    def check_order(self, flight, customer):
        # check if flight dates overlapp users flights
        cross_flights = self._repository.get_customer_cross_flight(customer.id, flight.id)
        if len(cross_flights) > 0:
            cross_flight = cross_flights[0]
            raise NotValidOrderException('You Have another flight on the same time!', Reason.CROSS_FLIGHT)
        # check if flight already departured
        order_date = datetime.now()
        departure_date = flight.departure_time
        if order_date > departure_date:
            raise NotValidOrderException(f'Flight Allready Departured at {departure_date}',
                                         Reason.FLIGHT_ALLREADY_DEPARTURED)
        # check if availiavle tickets
        availiable_tickets = flight.remaining_tickets
        if availiable_tickets <= 0:
            raise NotValidOrderException('Flight is sold out!', Reason.FLIGHT_SOLD_OUT)

    def check_cancel_order(self, ticket):
        flight = self.get_flight_by_id(ticket.flight_id)
        if flight is None:
            raise NotFoundException('Flight Not Found', Entity.FLIGHT, ticket.flight_id)
        cancel_time = datetime.now()
        if cancel_time > flight.departure_time:
            raise NotValidOrderException(f'Flight Allready Departured at {flight.departure_time}',
                                         Reason.FLIGHT_ALLREADY_DEPARTURED)

    def remove_ticket(self, ticket_id, flight: Flight):
        new_remaining_tickets = flight.remaining_tickets + 1
        self._repository.remove_ticket(ticket_id, flight.id, new_remaining_tickets)

    def add_ticket(self, ticket, flight: Flight):
        new_remaining_tickets = flight.remaining_tickets - 1
        self._repository.add_ticket(ticket, new_remaining_tickets)

    def get_ticket_by_id(self, ticket_id):
        ticket = self._repository.get_by_id(Ticket, ticket_id)
        return ticket

    def get_tickets_by_customer(self, customer_id):
        tickets = self._repository.get_tickets_by_customer(customer_id)
        return tickets

    def get_tickets_by_flight(self, flight_id):
        condition = (lambda query: query.filter(Ticket.flight_id == flight_id))
        tickets = self._repository.get_all_by_condition(Ticket, condition)
        return tickets

    def get_ticket_by_customer_fligth(self, flight_id, customer_id):
        ticket_cond = (lambda query: query.filter(Ticket.customer_id == customer_id,
                                                  Ticket.flight_id == flight_id))
        tickets = self._repository.get_all_by_condition(Ticket, ticket_cond)
        return tickets

