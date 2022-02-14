import os
from root import ROOT_DIR
from dataAccess.FlightRepository import FilghtRepository
from common.entities.db_config import local_session
from sqlalchemy import text


def load_db_scripts():
    repo = FilghtRepository(local_session)
    script_files_list = [
        os.path.join(ROOT_DIR, 'common/store_procedures/get_airline_by_username.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/get_arrival_flights.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/get_cusotmer_by_username.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/get_departure_flights.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/get_flights_by_airline_id.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/get_flights_by_parameters.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/get_overlapped_filghts.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/get_tickets_by_customer.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/get_user_by_username.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/get_administrator_by_username.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/get_flights_by_customer.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/remove_airline.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/remove_customer.sql'),
        os.path.join(ROOT_DIR, 'common/store_procedures/remove_administrator.sql')
    ]

    for file in script_files_list:
        script_file = open(file, 'r')
        script = text(script_file.read())
        script_file.close()
        repo.execute_script(script)

    local_session.commit()

