from common.entities.db_config import local_session, create_all_entities
from common.entities.Country import Country
from common.entities.AirlineCompany import AirlineCompany
from common.entities.Flight import Flight
from common.entities.UserRole import UserRole
from common.entities.User import User
from common.entities.Administrator import Administrator
from common.entities.Customer import Customer
from common.entities.Ticket import Ticket
from dataAccess.FlightRepository import FilghtRepository
from sqlalchemy.sql.expression import func


def main():
    try:
        create_all_entities()

        repo = FilghtRepository(local_session)

        print(repo.get_all(Country))

        # repo.update(Country, 'id', 1, dict(name='Brazil'))
        #
        # print(repo.get_all(Country))

        # update_cond = (lambda query: query.filter(Country.name == 'Brazil'))
        # repo.update_all_by_condition(Country, update_cond, dict(name='Canada'))
        #
        # print(repo.get_all(Country))
        # repo.remove(Country, 'id', 3)

        # print(repo.get_all(Country))

        # delete_cond = (lambda query: query.filter(Country.name == 'Italy'))
        # repo.remove_all_by_condition(Country, delete_cond)

        # print(repo.get_all(Country))

    except Exception as e:
        print(f'Error! : {str(e)}')


main()

