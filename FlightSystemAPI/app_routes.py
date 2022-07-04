import threading
# from flask_cors import CORS
# from flask import Flask, app, render_template, request, redirect, Blueprint
from common.entities.db_config import local_session, create_all_entities, connection_string
from common.entities.db_conifg_procedured import load_db_scripts
# from FlightSystemAPI.adminController import admin_blue_print
# from FlightSystemAPI.airlineController import airline_blue_print
# from FlightSystemAPI.customerController import customer_blue_print
# from FlightSystemAPI.anonymController import anonym_blue_print
# from FlightSystemAPI.handleRequests import HandleRequests
# from FlightSystemAPI.poolCorrelationEvents import PoolCorrelationEvents
from FlightSystemAPI.manageConsumers import ManageConsumners
from configparser import ConfigParser
from root import ROOT_DIR
import os

# INIT CONFIG
# config_file_name = 'config.conf'
# config_file_location = os.path.join(ROOT_DIR, config_file_name)
# config = ConfigParser()
# config.read(config_file_location)
#
# POOL_MAX_SIZE = 50

# app = Flask(__name__)
# cors = CORS(app)

# poolEvents = PoolCorrelationEvents(POOL_MAX_SIZE)
# create_req = HandleRequests(poolEvents)
# create_req.init_channels()

# app.register_blueprint(admin_blue_print(create_req))
# app.register_blueprint(airline_blue_print(create_req))
# app.register_blueprint(customer_blue_print(create_req))
# app.register_blueprint(anonym_blue_print(config, create_req))

create_all_entities()
load_db_scripts()

manageConsumers = ManageConsumners(local_session)
manageConsumers.init_consumers()

# app.run()

