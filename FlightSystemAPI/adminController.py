from flask import Blueprint, request, make_response, jsonify
from FlightSystemAPI.tokenRequired import token_required
from FlightSystemAPI.requestValidation import RequestValidation
from common.constants.enums import Actions, UserRoles
import json


def admin_blue_print(requests):
    blue_print = Blueprint('adminController', __name__)

    @blue_print.route('/admin/all_flights', methods=['GET'])
    @token_required
    def get_all_flights(token, *args, **kwargs):
        # (PAYLOAD)
        try:
            data = {'token': token}
            payload = {'facade_name': 'admin', 'action_id': Actions.GET_ALL_FLIGHTS, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                       {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/admin/flight/<flight_id>', methods=['GET'])
    @token_required
    def get_flight_by_id(token, *args, **kwargs):
        try:
            flight_id = kwargs['flight_id']
            is_form_valid = RequestValidation.validate_integer(flight_id)
            if not is_form_valid:
                # 400
                no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
                return no_form_res
            # (PAYLOAD)
            data = {'token': token, 'id': int(flight_id)}
            payload = {'facade_name': 'admin', 'action_id': Actions.GET_FLIGHT_BY_ID, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                       {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/admin/airlines', methods=['GET'])
    @token_required
    def get_all_airlines(token, *args, **kwargs):
        # (PAYLOAD)
        try:
            data = {'token': token}
            payload = {'facade_name': 'admin', 'action_id': Actions.GET_ALL_AIRLINES, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                       {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/admin/airline/<airline_id>', methods=['GET'])
    @token_required
    def get_airline_by_id(token, *args, **kwargs):
        try:
            airline_id = kwargs['airline_id']
            # req_args_keys = [('id', int)]
            is_form_valid = RequestValidation.validate_integer(airline_id)
            if not is_form_valid:
                # 400
                no_form_res = make_response('Missing Valued', 400,
                                            {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
                return no_form_res
        # (PAYLOAD)
            data = {'token': token, 'id': int(airline_id)}
            payload = {'facade_name': 'admin', 'action_id': Actions.GET_AIRLINE_BY_ID, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                       {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/admin/airlines_par', methods=['GET'])
    @token_required
    def get_airlines_by_parameters(token, *args, **kwargs):
        try:
            req_form_keys = [('country_id', int), ('name', str)]
            is_form_valid = RequestValidation.validate_form(request, req_form_keys)
            if not is_form_valid:
                # 400
                no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
                return no_form_res
            # (PAYLOAD)
            data = {'token': token, 'country_id': int(request.form['country_id']), 'name': request.form['name']}
            payload = {'facade_name': 'admin', 'action_id': Actions.GET_AIRLINES_BY_PARAMS, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                       {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/admin/countries', methods=['GET'])
    @token_required
    def get_all_countries(token, *args, **kwargs):
        try:
            # (PAYLOAD)
            data = {'token': token}
            payload = {'facade_name': 'admin', 'action_id': Actions.GET_ALL_COUNTRIES, 'data': data}
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
    @blue_print.route('/admin/all_customers', methods=['GET'])
    @token_required
    def get_all_customers(token, *args, **kwargs):
        # (PAYLOAD)
        data = {'token': token}
        payload = {'facade_name': 'admin', 'action_id': Actions.GET_ALL_CUSTOMERS, 'data': data}
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

    @blue_print.route('/admin/customers', methods=['POST'])
    @token_required
    def add_customer(token, *args, **kwargs):
        req_form_keys = [('username', str), ('password',  str), ('email', str),
                         ('first_name', str), ('last_name', str), ('address', str),
                         ('phone_number', str), ('credit_card_number', str)]
        is_form_valid = RequestValidation.validate_form(request, req_form_keys)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {
            'token': token,
            'customer': {
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
        payload = {'facade_name': 'admin', 'action_id': Actions.ADD_CUSTOMER, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            no_return_response = make_response('Succesfuly Commited!', 201)
            return no_return_response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                            {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/admin/customers/<customer_id>', methods=['DELETE'])
    @token_required
    def remove_customer(token, *args, **kwargs):
        customer_id = kwargs['customer_id']
        is_form_valid = RequestValidation.validate_integer(customer_id)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {'token': token, 'customer_id': int(customer_id)}
        payload = {'facade_name': 'admin', 'action_id': Actions.REMOVE_CUSTOMER, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            response = make_response('Succesfuly Commited', 204)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                            {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/admin/airlines', methods=['POST'])
    @token_required
    def add_airline(token, *args, **kwargs):
        req_form_keys = [('username', str), ('password', str), ('email', str), ('name', str), ('country_id', int)]
        is_form_valid = RequestValidation.validate_form(request, req_form_keys)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {
            'token': token,
            'airline': {
                'id': None,
                'name': request.form['name'],
                'country_id': request.form['country_id'],
                'user_id': None
            },
            'user': {
                'id': None,
                'username': request.form['username'],
                'password': request.form['password'],
                'email': request.form['email'],
                'user_role': UserRoles.AIRLINE
            }}
        payload = {'facade_name': 'admin', 'action_id': Actions.ADD_AIRLINE, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            no_return_response = make_response('Succesfuly Commited!', 201)
            return no_return_response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                            {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/admin/airlines/<airline_id>', methods=['DELETE'])
    @token_required
    def remove_airline(token, *args, **kwargs):
        airline_id = kwargs['airline_id']
        is_form_valid = RequestValidation.validate_integer(airline_id)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {'token': token, 'airline_id': int(airline_id)}
        payload = {'facade_name': 'admin', 'action_id': Actions.REMVOE_AIRLINE, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            response = make_response('Succesfuly Commited', 204)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                            {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/admin/admins', methods=['POST'])
    @token_required
    def add_administrator(token, *args, **kwargs):
        req_form_keys = [('username', str), ('password', str), ('email', str),
                         ('first_name', str), ('last_name', str)]
        is_form_valid = RequestValidation.validate_form(request, req_form_keys)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {
            'token': token,
            'administrator': {
                'id': None,
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'user_id': None
            },
            'user': {
                'id': None,
                'username': request.form['username'],
                'password': request.form['password'],
                'email': request.form['email'],
                'user_role': UserRoles.ADMINISTATOR
            }}
        payload = {'facade_name': 'admin', 'action_id': Actions.ADD_ADMINISTRATOR, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            no_return_response = make_response('Succesfuly Commited!', 201)
            return no_return_response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/admin/admins/<admin_id>', methods=['DELETE'])
    @token_required
    def remove_administrator(token, *args, **kwargs):
        admin_id = kwargs['admin_id']
        is_form_valid = RequestValidation.validate_integer(admin_id)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {'token': token, 'administrator_id': int(admin_id)}
        payload = {'facade_name': 'admin', 'action_id': Actions.REMOVE_ADMINISTRATOR, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            response = make_response('Succesfuly Commited', 204)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response
    return blue_print



