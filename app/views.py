# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, jsonify
import sys
import sqlite3_db


reload(sys)
sys.setdefaultencoding('utf8')


@app.route('/', methods=['GET', 'POST'])
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
