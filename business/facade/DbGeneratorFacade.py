from business.facade.facadeBase import FacadeBase
from common.constants.enums import Field, Actions, Reason, Entity
from common.exceptions.notFoundException import NotFoundException
from common.exceptions.notUniqueException import NotUniqueException
from common.exceptions.notValidInputException import NotVaildInputException
from common.exceptions.notValidOrderException import NotValidOrderException
from common.exceptions.notValidFlightException import NotValidFlightException


class BdGeneratorFacade(FacadeBase):
    def __init__(self, local_session):
        super().__init__(local_session)

    def add_country(self, country):
        try:
            exist_country = self._airlineService.get_country_by_name(country.name)
            if len(exist_country) > 0:
                raise NotUniqueException('Country allready Exists!', Actions.ADD_AIRLINE, Field.AIRLINE_COUNTRY_ID, country.id)
            self._airlineService.add_country(country)
        except Exception as exc:
            self.handle_exception(Actions.REMOVE_ADMINISTRATOR, exc)

    def add_administrator(self, administrator, user):
        try:
            user = user.adapt_str()
            administrator.adapt_str()
            self._loginService.validate_new_user(user)
            self._airlineService.validate_administrator(administrator)
            self._airlineService.add_administrator(administrator, user)
        except Exception as exc:
            self.handle_exception(Actions.REMOVE_ADMINISTRATOR, exc)

    def add_airline(self, airline, user):
        try:
            user = user.adapt_str()
            airline.adapt_str()
            self._loginService.validate_new_user(user)
            self._airlineService.validate_airline(airline)
            self._airlineService.add_airline(airline, user)
        except Exception as exc:
            self.handle_exception(Actions.REMOVE_ADMINISTRATOR, exc)

    def add_customer(self, customer, user):
        try:
            # CREATE USER
            user = user.adapt_str()
            customer.adapt_str()
            # OK - CREATE CUSTOMER
            self._loginService.validate_new_user(user)
            self._customerService.validate_customer(customer)
            self._customerService.add_customer(customer, user)
        except Exception as exc:
            self.handle_exception(Actions.ADD_CUSTOMER, exc)

    def add_flight(self, flight):
        try:
            self._airlineService.validate_flight(flight)
            self._airlineService.add_fligth(flight)
        except Exception as exc:
            # match_exception = BdGeneratorFacade.is_not_matched_exception(exc)
            # if match_exception:
            #     return False
            self.handle_exception(Actions.ADD_FLIGHT, exc)

    def add_ticket(self, ticket):
        try:
            # check flight
            flight = self.get_flight_by_id(ticket.flight_id)
            if flight is None:
                raise NotFoundException('Flight Not Found', Entity.FLIGHT, ticket.flight_id)
            # check customer
            customer = self._customerService.get_customer_by_id(ticket.customer_id)
            if customer is None:
                raise NotFoundException('Customer Not Found', Entity.CUSTOMER, ticket.customer_id)
            # check order
            exists_ticket = self._ordersService.get_ticket_by_customer_fligth(ticket.flight_id, ticket.customer_id)
            if len(exists_ticket) > 0:
                raise NotUniqueException(f'Ticket with customer {ticket.customer_id} and '
                                         f'flight {ticket.flight_id} allready exists',
                                         Actions.ADD_TICKET,
                                         Field.CUSTOMER_ID,
                                         f'{ticket.flight_id}-{ticket.customer_id}'
                                         )
            self._ordersService.check_order(flight, customer)
            # add tickets and #  remove ticket from flight remaing tickets
            self._ordersService.add_ticket(ticket, flight)
            return True
        except Exception as exc:
            match_exception = BdGeneratorFacade.is_not_matched_exception(exc)
            if match_exception:
                return False
            self.handle_exception(Actions.ADD_TICKET, exc)

    def get_all_customers(self):
        try:
            customers = self._customerService.get_all_customers()
            return customers
        except Exception as exc:
            self.handle_exception(Actions.GET_ALL_CUSTOMERS, exc)

    @staticmethod
    def is_not_matched_exception(exc):
        not_matched_exception = isinstance(exc, NotVaildInputException) \
              or isinstance(exc, NotFoundException) \
              or isinstance(exc, NotUniqueException) \
              or isinstance(exc, NotValidOrderException) \
              or isinstance(exc, NotValidFlightException)
        return not_matched_exception
