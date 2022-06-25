from flask import Blueprint, request, make_response, jsonify
from common.constants.enums import Actions, UserRoles
from FlightSystemAPI.requestValidation import RequestValidation
from datetime import datetime, timedelta
import jwt
import json


def anonym_blue_print(config, requests):
    blue_print = Blueprint('anonymController', __name__)

    @blue_print.route('/anonym/all_flights', methods=['GET'])
    def get_all_flights():
        # (PAYLOAD)
        try:
            payload = {'facade_name': 'anonym', 'action_id': Actions.GET_ALL_FLIGHTS, 'data': None}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                   {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/anonym/flight/<flight_id>', methods=['GET'])
    def get_flight_by_id(flight_id):
        is_form_valid = RequestValidation.validate_integer(flight_id)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {'id': int(flight_id)}
        payload = {'facade_name': 'anonym', 'action_id': Actions.GET_FLIGHT_BY_ID, 'data': data}
        try:
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                   {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/anonym/airlines', methods=['GET'])
    def get_all_airlines():
        # (PAYLOAD)
        try:
            payload = {'facade_name': 'anonym', 'action_id': Actions.GET_ALL_AIRLINES, 'data': None}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                   {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/anonym/airline/<airline_id>', methods=['GET'])
    def get_airline_by_id(airline_id):
        is_form_valid = RequestValidation.validate_integer(airline_id)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {'id': int(airline_id)}
        payload = {'facade_name': 'anonym', 'action_id': Actions.GET_AIRLINE_BY_ID, 'data': data}
        try:
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                   {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/anonym/airlines_par', methods=['GET'])
    def get_airlines_by_parameters():
        try:
            req_form_keys = [('country_id', int), ('name', str)]
            is_form_valid = RequestValidation.validate_form(request, req_form_keys)
            if not is_form_valid:
                # 400
                no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
                return no_form_res
            # (PAYLOAD)
            data = {'country_id': request.form['country_id'], 'name': request.form['name']}
            payload = {'facade_name': 'anonym', 'action_id': Actions.GET_AIRLINES_BY_PARAMS, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                       {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/anonym/countries', methods=['GET'])
    def get_all_countries():
        # (PAYLOAD)
        try:
            data = None
            payload = {'facade_name': 'anonym', 'action_id': Actions.GET_ALL_COUNTRIES, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                       {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    # *********************************************************************
    @blue_print.route('/anonym/login', methods=['POST'])
    def login():
        # IS FORM
        req_form_keys = [('username', str), ('password', str)]
        is_form_valid = RequestValidation.validate_form(request, req_form_keys)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # VALID FORM
        form_data = request.form
        username = form_data['username']
        password = form_data['password']
        data = {'username': username, 'password': password}
        payload = {'facade_name': 'anonym', 'action_id': Actions.LOGIN, 'data': data}
        # LOGIN
        try:
            correl_id = requests.send_request(payload, True)
            # time.sleep(1)
            identity_token = requests.get_response(correl_id)
            # CREATE TOKEN
            secret_key = config['security']['secret_key']
            token = jwt.encode({
                'user_name': identity_token['user_name'],
                'user_role_id': identity_token['user_role_id'],
                'identity_id': identity_token['identity_id'],
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, secret_key)
            auth_res = make_response(jsonify({'token': token.decode('utf-8')}), 200)
            return auth_res
        except Exception as exc:
            login_error_rep = make_response(f'Not Authorized! {str(exc)}', 401,
                                                {'WWW-Authenticate': f'Basic realm="Not Authorized!"'})
            return login_error_rep

    @blue_print.route('/anonym/cust', methods=['POST'])
    def add_customer():
        req_form_keys = [('username', str), ('password', str), ('email', str),
                         ('first_name', str), ('last_name', str), ('address', str),
                         ('phone_number', str), ('credit_card_number', str)]
        is_form_valid = RequestValidation.validate_form(request, req_form_keys)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {'customer': {
            'id': None,
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'address': request.form['address'],
            'phone_number': request.form['phone_number'],
            'credit_card_number': request.form['credit_card_number'],
            'user_id': None
        },
            'user': {
            'id': None,
            'username': request.form['username'],
            'password': request.form['password'],
            'email': request.form['email'],
            'user_role': UserRoles.CUSTOMER
        }}
        payload = {'facade_name': 'anonym', 'action_id': Actions.ADD_CUSTOMER, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            no_return_response = make_response('Succesfuly Commited!', 201)
            return no_return_response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response
    return blue_print
