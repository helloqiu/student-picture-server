# -*- coding: utf-8 -*-
from datetime import timedelta
from app import app
from flask import render_template, make_response, request, current_app, jsonify
from functools import update_wrapper
import sys
import sqlite3_db


reload(sys)
sys.setdefaultencoding('utf8')


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/', methods=['GET', 'POST'])
@crossdomain(origin='*')
def getInfoView():
    studentid = request.form['studentid']
    name = request.form['name']
    if (name == '' and studentid == ''):
        return 'ERROR'
    if (studentid != ''):
        query = 'select * from student where studentid=\'%s\'' % studentid
    else:
        query = 'select * from student where name=\'%s\'' % name
    cur = sqlite3_db.connect_db().execute(query)
    rv = cur.fetchall()
    cur.close()
    if rv is None:
        return 'ERROR FIND'
    rv = rv[0]
    name = rv[1]
    studentid = rv[2]
    sex = rv[3]
    socialid = rv[4]
    special = rv[5]
    college = rv[6]
    return jsonify(
        {
            "name": name,
            "studentid": studentid,
            "sex": sex,
            "socialid": socialid,
            "special": special,
            "college": college
        })
