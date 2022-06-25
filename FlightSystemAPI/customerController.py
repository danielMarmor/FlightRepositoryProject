from flask import Blueprint, request, make_response, jsonify
from FlightSystemAPI.tokenRequired import token_required
from FlightSystemAPI.requestValidation import RequestValidation
from common.constants.enums import Actions, UserRoles
import json


def customer_blue_print(requests):
    blue_print = Blueprint('customerController', __name__)

    @blue_print.route('/cust/all_flights', methods=['GET'])
    @token_required
    def get_all_flights(token, *args, **kwargs):
        # (PAYLOAD)
        try:
            data = {'token': token}
            payload = {'facade_name': 'cust', 'action_id': Actions.GET_ALL_FLIGHTS, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/cust/flight/<flight_id>', methods=['GET'])
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
            payload = {'facade_name': 'cust', 'action_id': Actions.GET_FLIGHT_BY_ID, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/cust/airlines', methods=['GET'])
    @token_required
    def get_all_airlines(token, *args, **kwargs):
        # (PAYLOAD)
        try:
            data = {'token': token}
            payload = {'facade_name': 'cust', 'action_id': Actions.GET_ALL_AIRLINES, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/cust/airline/<airline_id>', methods=['GET'])
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
            payload = {'facade_name': 'cust', 'action_id': Actions.GET_AIRLINE_BY_ID, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/cust/airlines_par', methods=['GET'])
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
            payload = {'facade_name': 'cust', 'action_id': Actions.GET_AIRLINES_BY_PARAMS, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/cust/countries', methods=['GET'])
    @token_required
    def get_all_countries(token, *args, **kwargs):
        try:
            # (PAYLOAD)
            data = {'token': token}
            payload = {'facade_name': 'cust', 'action_id': Actions.GET_ALL_COUNTRIES, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/cust/customer', methods=['PUT'])
    @token_required
    def update_customer(token, *args, **kwargs):
        req_form_keys = [('id', int), ('first_name', str), ('last_name', str), ('address', str),
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
            'customer_id': int(request.form['id']),
            'customer': {
                'id': int(request.form['id']),
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'address': request.form['address'],
                'phone_number': request.form['phone_number'],
                'credit_card_number': request.form['credit_card_number'],
                'user_id': None
            }}
        payload = {'facade_name': 'cust', 'action_id': Actions.UPDATE_CUSTOMER, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            no_return_response = make_response('Succesfuly Commited!', 204)
            return no_return_response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/cust/tickets', methods=['POST'])
    @token_required
    def add_ticket(token, *args, **kwargs):
        req_form_keys = [('flight_id', int), ('customer_id', int)]
        is_form_valid = RequestValidation.validate_form(request, req_form_keys)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {
            'token': token,
            'ticket': {
                'flight_id': int(request.form['flight_id']),
                'customer_id': int(request.form['customer_id'])
            }}
        payload = {'facade_name': 'cust', 'action_id': Actions.ADD_TICKET, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            no_return_response = make_response('Succesfuly Commited!', 201)
            return no_return_response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/cust/tickets/<ticket_id>', methods=['DELETE'])
    @token_required
    def remove_ticket(token, *args, **kwargs):
        ticket_id = kwargs['ticket_id']
        is_form_valid = RequestValidation.validate_integer(ticket_id)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {'token': token, 'ticket_id': int(ticket_id)}
        payload = {'facade_name': 'cust', 'action_id': Actions.REMOVE_TICKET, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            response = make_response('Succesfuly Commited', 204)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/cust/tickets/<customer_id>', methods=['GET'])
    @token_required
    def get_my_tickets(token, *args, **kwargs):
        customer_id = kwargs['customer_id']
        is_form_valid = RequestValidation.validate_integer(customer_id)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {'token': token, 'customer_id': int(customer_id)}
        payload = {'facade_name': 'cust', 'action_id': Actions.GET_TICKETS_BY_CUSTOMER, 'data': data}
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

    return blue_print
    # *********************************************************************








