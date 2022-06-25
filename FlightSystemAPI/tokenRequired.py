from flask import Flask, request, make_response
from functools import wraps
from configparser import ConfigParser
from root import ROOT_DIR

import jwt
import os

# INIT CONFIG
config_file_name = 'config.conf'
config_file_location = os.path.join(ROOT_DIR, config_file_name)
config = ConfigParser()
config.read(config_file_location)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        is_auth = 'Authorization' in request.headers
        if not is_auth:
            token_missing_res = make_response('Token is missing!', 401)
            return token_missing_res
        # AUTHORIZATION
        token = request.headers['Authorization']
        token = token.removeprefix('Bearer ')
        secret_key = config['security']['secret_key']
        try:
            auth_data = jwt.decode(token, secret_key)
        except:
            invalid_token_res = make_response('Token is Invalid!', 401)
            return invalid_token_res
        # CHECK TOKEN CONTENT:
        is_token = 'identity_id' in auth_data.keys() and \
                   'user_name' in auth_data.keys() and \
                   'user_role_id' in auth_data.keys()
        if not is_token:
            invalid_token_res = make_response('Token is Invalid!', 401)
            return invalid_token_res
        # RETURN
        target = f(auth_data, *args, **kwargs)
        return target
    return decorated

