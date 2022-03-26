from datetime import datetime, timedelta
from common.entities.User import User
from common.entities.AirlineCompany import AirlineCompany
from common.entities.Country import Country
from common.entities.Customer import Customer
from common.entities.Flight import Flight
from common.entities.Ticket import Ticket
from common.entities.UserRole import UserRole
from common.entities.Administrator import Administrator
import time


class TestService:
    def __init__(self, local_sesion, repository):
        self.local_sesion = local_sesion
        self._repository = repository

    def restore_database(self):
        self._repository.reset_table_auto_incerement(Ticket)
        self._repository.reset_table_auto_incerement(Customer)
        self._repository.reset_table_auto_incerement(Flight)
        self._repository.reset_table_auto_incerement(Administrator)
        self._repository.reset_table_auto_incerement(AirlineCompany)
        self._repository.reset_table_auto_incerement(User)
        self._repository.reset_table_auto_incerement(UserRole)
        self._repository.reset_table_auto_incerement(Country)

        self._repository.commit()

        initial_user_roles = [
            UserRole(role_name='Customer'),
            UserRole(role_name='AirlineCompany'),
            UserRole(role_name='Administrator')
        ]

        initial_users = [
            # id = 1
            User(username='Daniel1221', password='12345678', email='danielmarmor2@gmail.com',
                 user_role=1),
            # id = 2
            User(username='Stav1221', password='8765432X', email='stavmarmor@gmail.com',
                 user_role=1),
            # id = 3
            User(username='Itay1221', password='13243546', email='itaymarmor@gmail.com',
                 user_role=1),
            # id = 4
            User(username='SonySock', password='1449939GG', email='sonySock@gmail.com',
                 user_role=1),
            # id = 5
            User(username='amair123', password='019920098$3', email='amairlines@gmail.com',
                 user_role=2),
            # id = 6
            User(username='swiss123', password='015180098$3', email='swissair@gmail.com',
                 user_role=2),
            # id = 7 british airways
            User(username='british123', password='016677098$3', email='britishairways@gmail.com',
                 user_role=2),
            # id = 8 --
            User(username='shimi1029', password='BBB2930440', email='shimitavori@gmail.com',
                 user_role=3),
            # id = 9 --
            User(username='danielma', password='danielma440', email='danieluswer@gmail.com',
                 user_role=3),
            # id = 10 --
            User(username='natalia', password='natalia222', email='natalia@gmail.com',
                 user_role=3)
        ]
        initial_administrators = [
            Administrator(first_name='Daniel', last_name='Marmor', user_id=9),
            Administrator(first_name='Natalia', last_name='Tomakin', user_id=10)
        ]
        initial_customers = [
            Customer(
                first_name='Daniel',
                last_name='Marmor',
                address='Ben tzvi 3 K.motzkin',
                phone_number='0543675402',
                credit_card_number='1099-1111-2314-1234',
                user_id=1),
            Customer(
                first_name='Stav',
                last_name='Marmor',
                address='Benjamin Hevron',
                phone_number='0502224730',
                credit_card_number='1070-1322-2828-1524',
                user_id=2),
            Customer(
                first_name='Itay',
                last_name='Marmor',
                address='Roky Mountain 456 Californail',
                phone_number='052400300',
                credit_card_number='1078-1455-8213-5567',
                user_id=3)

        ]

        initial_countries = [
            # id = 1
            Country(name='United States'),
            # id = 2
            Country(name='Israel'),
            # id = 3
            Country(name='Germany'),
            # id = 4
            Country(name='United Kingdom')
        ]
        initial_airlines = [
            # id = 1
            AirlineCompany(name='American Airlines', country_id=1, user_id=5),
            # id = 2
            AirlineCompany(name='British Airways', country_id=4, user_id=7)
        ]
        days_ahead_security_date = datetime.today() + timedelta(days=3)
        allready_departued_date = datetime.today() + timedelta(days=-2)
        initial_flights = [
            # id =1 ==> already departured
            Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                   departure_time=datetime(allready_departued_date.year, allready_departued_date.month,
                                           allready_departued_date.day, 12, 0, 0),
                   landing_time=datetime(2022, 1, 14, 21, 0, 0),
                   remaining_tickets=1),
            # id =2 ==> positive
            Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                   departure_time=datetime(2022, 1, 23, 7, 0, 0),
                   landing_time=datetime(2022, 1, 23, 18, 0, 0),
                   remaining_tickets=1),

            # id =3 ==> sold out
            Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                   departure_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                           days_ahead_security_date.day, 0, 30, 0),
                   landing_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                         days_ahead_security_date.day, 11, 30, 0),
                   remaining_tickets=0),

            # id =4 ==> positive
            Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                   departure_time=datetime(2022, 2, 2, 0, 30, 0),
                   landing_time=datetime(2022, 2, 2, 11, 30, 0),
                   remaining_tickets=25),
            # id =5 ==> positive
            Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                   departure_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                           days_ahead_security_date.day, 0, 30, 0),
                   landing_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                         days_ahead_security_date.day, 11, 30, 0),
                   remaining_tickets=25),

            # id =6 ==> positive
            Flight(airline_company_id=1, origin_country_id=2, destination_country_id=1,
                   departure_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                           days_ahead_security_date.day, 11, 45, 0),
                   landing_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                         days_ahead_security_date.day, 23, 15, 0),
                   remaining_tickets=14),
            # id =7 ==> positive
            Flight(airline_company_id=2, origin_country_id=2, destination_country_id=1,
                   departure_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                           days_ahead_security_date.day, 11, 45, 0),
                   landing_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                         days_ahead_security_date.day, 17, 15, 0),
                   remaining_tickets=100),
            # id =8 ==> positive
            Flight(airline_company_id=2, origin_country_id=1, destination_country_id=2,
                   departure_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                           days_ahead_security_date.day, 18, 30, 0),
                   landing_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                         days_ahead_security_date.day, 23, 50, 0),
                   remaining_tickets=200),

            # id =9 ==> positive
            Flight(airline_company_id=2, origin_country_id=1, destination_country_id=2,
                   departure_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                           days_ahead_security_date.day, 6, 30, 0),
                   landing_time=datetime(days_ahead_security_date.year, days_ahead_security_date.month,
                                         days_ahead_security_date.day, 12, 0, 0),
                   remaining_tickets=36)
        ]

        initial_tickets = [
            # id= 1
            Ticket(flight_id=7, customer_id=2),
            # id= 2 with flight depatrured
            Ticket(flight_id=1, customer_id=3),
            # id= 3
            Ticket(flight_id=4, customer_id=3),
            # id= 4
            Ticket(flight_id=4, customer_id=2)
        ]

        self._repository.add_all(initial_user_roles)
        self._repository.add_all(initial_countries)
        self._repository.add_all(initial_users)
        self._repository.add_all(initial_administrators)
        self._repository.add_all(initial_airlines)
        self._repository.add_all(initial_flights)
        self._repository.add_all(initial_customers)
        self._repository.add_all(initial_tickets)

        self._repository.commit()

    def restore_database_no_recreate(self, is_delete):
        if is_delete:
            self._repository.reset_table_auto_incerement(Ticket)
            self._repository.reset_table_auto_incerement(Customer)
            self._repository.reset_table_auto_incerement(Flight)
            self._repository.reset_table_auto_incerement(Administrator)
            self._repository.reset_table_auto_incerement(AirlineCompany)
            self._repository.reset_table_auto_incerement(User)
            self._repository.reset_table_auto_incerement(UserRole)
            self._repository.reset_table_auto_incerement(Country)
            self._repository.commit()

            initial_user_roles = [
                UserRole(role_name='Customer'),
                UserRole(role_name='AirlineCompany'),
                UserRole(role_name='Administrator')
            ]
            self._repository.add_all(initial_user_roles)
            self._repository.commit()
        else:
            countries = self._repository.get_all(Country)
            if len(countries) == 0:
                self._repository.reset_table_auto_incerement(Country)

            user_roles = self._repository.get_all(UserRole)
            if len(user_roles) == 0:
                self._repository.reset_table_auto_incerement(UserRole)
                initial_user_roles = [
                    UserRole(role_name='Customer'),
                    UserRole(role_name='AirlineCompany'),
                    UserRole(role_name='Administrator')
                ]
                self._repository.add_all(initial_user_roles)

            self._repository.commit()
