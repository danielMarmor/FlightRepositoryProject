from flask import Blueprint, make_response, request
from FlightSystemAPI.tokenRequired import token_required
from common.constants.enums import Actions, UserRoles
from FlightSystemAPI.requestValidation import RequestValidation
import json


def airline_blue_print(requests):
    blue_print = Blueprint('airlineController', __name__)

    @blue_print.route('/airline/all_flights', methods=['GET'])
    @token_required
    def get_all_flights(token, *args, **kwargs):
        # (PAYLOAD)
        try:
            data = {'token': token}
            payload = {'facade_name': 'airline', 'action_id': Actions.GET_ALL_FLIGHTS, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/airline/flight/<flight_id>', methods=['GET'])
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
            payload = {'facade_name': 'airline', 'action_id': Actions.GET_FLIGHT_BY_ID, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/airline/airlines', methods=['GET'])
    @token_required
    def get_all_airlines(token, *args, **kwargs):
        # (PAYLOAD)
        try:
            data = {'token': token}
            payload = {'facade_name': 'airline', 'action_id': Actions.GET_ALL_AIRLINES, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/airline/airline/<airline_id>', methods=['GET'])
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
            payload = {'facade_name': 'airline', 'action_id': Actions.GET_AIRLINE_BY_ID, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/airline/airlines_par', methods=['GET'])
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
            payload = {'facade_name': 'airline', 'action_id': Actions.GET_AIRLINES_BY_PARAMS, 'data': data}
            correl_id = requests.send_request(payload, False)
            results = requests.get_response(correl_id)
            serialized_value = json.dumps(results)
            response = make_response(serialized_value, 200)
            return response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/airline/countries', methods=['GET'])
    @token_required
    def get_all_countries(token, *args, **kwargs):
        try:
            # (PAYLOAD)
            data = {'token': token}
            payload = {'facade_name': 'airline', 'action_id': Actions.GET_ALL_COUNTRIES, 'data': data}
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
    @blue_print.route('/airline/flights/<airline_id>', methods=['GET'])
    @token_required
    def get_my_flights(token, *args, **kwargs):
        airline_id = kwargs['airline_id']
        is_form_valid = RequestValidation.validate_integer(airline_id)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {'token': token, 'airline_id': int(airline_id)}
        payload = {'facade_name': 'airline', 'action_id': Actions.GET_FLIGHT_BY_AIRLINE, 'data': data}
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

    @blue_print.route('/airline/airlines', methods=['PUT'])
    @token_required
    def update_airline(token, *args, **kwargs):
        req_form_keys = [('id', int), ('name', str), ('country_id', int)]
        is_form_valid = RequestValidation.validate_form(request, req_form_keys)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {
            'token': token,
            'airline_id': int(request.form['id']),
            'airline': {
                'id': int(request.form['id']),
                'name': request.form['name'],
                'country_id': int(request.form['country_id']),
                'user_id': None
            }}
        payload = {'facade_name': 'airline', 'action_id': Actions.UPDATE_AIRLINE, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            no_return_response = make_response('Succesfuly Commited!', 204)
            return no_return_response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/airline/flights', methods=['POST'])
    @token_required
    # !!!!!! DATE SHOULD BE IN FORMAT 'YYYY-MM-DDDD'
    def add_flight(token, *args, **kwargs):
        req_form_keys = [('airline_company_id', int),
                         ('origin_country_id', int),
                         ('destination_country_id', int),
                         ('departure_date', str),
                         ('departure_hour', int),
                         ('departure_minute', int),
                         ('landing_date', str),
                         ('landing_hour', int),
                         ('landing_minute', int)]

        is_form_valid = RequestValidation.validate_form(request, req_form_keys)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {
            'token': token,
            'flight': {
                'id': None,
                'airline_company_id': int(request.form['airline_company_id']),
                'origin_country_id': int(request.form['origin_country_id']),
                'destination_country_id': int(request.form['destination_country_id']),
                'departure_date': str(request.form['departure_date']),
                'departure_hour': int(request.form['departure_hour']),
                'departure_minute': int(request.form['departure_minute']),
                'landing_date': str(request.form['landing_date']),
                'landing_hour': int(request.form['landing_hour']),
                'landing_minute': int(request.form['landing_minute'])
            }}
        payload = {'facade_name': 'airline', 'action_id': Actions.ADD_FLIGHT, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            no_return_response = make_response('Succesfuly Commited!', 201)
            return no_return_response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/airline/flights', methods=['PUT'])
    @token_required
    def update_flight(token, *args, **kwargs):
        req_form_keys = [('id', int),
                         ('airline_company_id', int),
                         ('origin_country_id', int),
                         ('destination_country_id', int),
                         ('departure_date', str),
                         ('departure_hour', int),
                         ('departure_minute', int),
                         ('landing_date', str),
                         ('landing_hour', int),
                         ('landing_minute', int),
                         ('remaining_tickets', int)]
        is_form_valid = RequestValidation.validate_form(request, req_form_keys)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {
            'token': token,
            'flight_id': int(request.form['id']),
            'flight': {
                'id': int(request.form['id']),
                'airline_company_id': int(request.form['airline_company_id']),
                'origin_country_id': int(request.form['origin_country_id']),
                'destination_country_id': int(request.form['destination_country_id']),
                'departure_date': str(request.form['departure_date']),
                'departure_hour': int(request.form['departure_hour']),
                'departure_minute': int(request.form['departure_minute']),
                'landing_date': str(request.form['landing_date']),
                'landing_hour': int(request.form['landing_hour']),
                'landing_minute': int(request.form['landing_minute']),
                'remaining_tickets': int(request.form['remaining_tickets'])
            }}
        payload = {'facade_name': 'airline', 'action_id': Actions.UPDATE_FLIGHT, 'data': data}
        try:
            correl_id = requests.send_request(payload, True)
            results = requests.get_response(correl_id)
            no_return_response = make_response('Succesfuly Commited!', 204)
            return no_return_response
        except Exception as exc:
            error_response = make_response(str(exc), 200,
                                           {'WWW-Authenticate': f'Basic realm="{str(exc)}"'})
            return error_response

    @blue_print.route('/airline/flights/<flight_id>', methods=['DELETE'])
    @token_required
    def remove_flight(token, *args, **kwargs):
        flight_id = kwargs['flight_id']
        is_form_valid = RequestValidation.validate_integer(flight_id)
        if not is_form_valid:
            # 400
            no_form_res = make_response('Missing Valued', 400,
                                        {'WWW-Authenticate': 'Basic realm="Missing Values!"'})
            return no_form_res
        # (PAYLOAD)
        data = {'token': token, 'flight_id': int(flight_id)}
        payload = {'facade_name': 'airline', 'action_id': Actions.REMOVE_FLIGHT, 'data': data}
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



