from flask import Flask, app, render_template, request, redirect
from business.facade.anonymousFacade import *
from common.entities.User import User
from common.entities.db_config import local_session, create_all_entities, connection_string
from common.entities.db_conifg_procedured import load_db_scripts

import os

template_dir = os.path.abspath('../templates')
app = Flask(__name__, template_folder=template_dir)
# app.static_folder = os.path.abspath('../static')

create_all_entities()
load_db_scripts()


@app.route('/', methods=['GET'])
def home():
    login_template = render_template('loginForm.html')
    return login_template


@app.route('/process_form', methods=['POST'])
def login():
    anonymous_facade = None
    facade = None
    user = None
    form_data = request.form
    if not form_data:
        return redirect('/error')
    is_form = 'uname' in form_data.keys() and 'psw' in form_data.keys()
    if not is_form:
        return redirect('/error')
    try:
        uname = form_data['uname']
        psw = form_data['psw']
        anonymous_facade = AnonymousFacade(local_session)
        facade = anonymous_facade.login(uname, psw)
        user = anonymous_facade.get_user_by_user_name(uname)
    except Exception as exc:
        return redirect('/error')
    if facade is None:
        return redirect('/error')
    if user is None:
        return redirect('/error')
    # LOGIN OK
    logged_in_template = render_template('loggedIn.html', user_id=str(user.id))
    return logged_in_template


@app.route('/error', methods=['GET'])
def error():
    error_template = render_template('errorPage.html')
    return error_template


app.run()