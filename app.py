#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, Response, render_template, jsonify
from functools import wraps
import sqlite3
import logging


app = Flask(__name__, static_url_path='/static')


#Configuration
uname = "admin"
pwd = "pass"

categories = [{'name': 'Category 1', 'id': '1'}, {'name': 'Category 2', 'id': '2'}]


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == uname and password == pwd


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials'
                    , 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'
                    })


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
#@requires_auth
def main():
    return render_template('send_ques.html', categories=categories,otherid = categories[len(categories)-1]["id"])

@app.route('/admin')
@requires_auth
def admin():
    #conn = sqlite3.connect("main.db")
    #cursor = conn.execute("SELECT ID,Text,status,fr,category from QUESTIONS")
    #questions = cursor.fetchall()
    lastid = 0
    #if(len(questions)>0):
    #    lastid = questions[len(questions) - 1][0]
    #print lastid
    #conn.close()
    #return render_template('admin.html',questions = questions, lastid = lastid, categories = categories)
    return render_template('admin.html',categories = categories)

@app.route('/display')
@requires_auth
def display():
    return render_template('display.html')

@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST' and request.form['question']:
        ques = request.form['question']
        category = request.form.get("categories",categories[len(categories)-1]["id"])
        name = request.form.get("name","Anonymous")
        if(request.form.get("anon",None)=="anon"):
            name = "Anonymous"
        t = (ques,category,name)
        print t
        conn = sqlite3.connect("main.db")
        conn.execute("INSERT INTO QUESTIONS (Text,status,category,fr,stamp) values(?,'none',?,?,DATETIME('now','localtime'))",t)
        conn.commit()
        conn.close()
        return render_template('send_response.html', message="Sent your question!")
    else:
        return render_template('send_response.html', message="Error sending your question, please check if you filled in fields correctly")

@app.route('/getques_display')
@requires_auth
def getques_display():
    conn = sqlite3.connect("main.db")
    cursor = conn.execute("SELECT ID,Text,fr from QUESTIONS_Pushed ORDER BY ID DESC")
    questions = cursor.fetchall()
    dict = {"questions":questions}
    conn.close()
    return jsonify(**dict)

@app.route('/getques')
@requires_auth
def getques():
    lastid = request.args.get('latest')
    conn = sqlite3.connect("main.db")
    cursor = conn.execute("SELECT ID,Text,status,fr,category from QUESTIONS where id>?",(lastid,))
    questions = cursor.fetchall()
    dict = {"questions":questions}
    conn.close()
    return jsonify(**dict)

@app.route('/delete')
@requires_auth
def dele():
    i = request.args.get('id')
    conn = sqlite3.connect("main.db")
    cursor = conn.execute("UPDATE QUESTIONS SET status='deleted' where id=?",(i,))
    if(cursor.rowcount == 1):
        conn.commit()
        conn.close()
        return "Success"
    else:
        conn.close()
        return "Failed"

@app.route('/push')
@requires_auth
def push():
    i = request.args.get('id')
    conn = sqlite3.connect("main.db")
    cursor = conn.execute("UPDATE QUESTIONS SET status='pushed' where id=?",(i,))
    if(cursor.rowcount == 1):
        conn.execute("INSERT INTO QUESTIONS_Pushed (Text,category,fr,stamp) SELECT Text,category,fr,DATETIME('now','localtime') FROM QUESTIONS where id=?",(i,))
        conn.commit()
        conn.close()
        return "Success"
    else:
        conn.close()
        return "Failed"

@app.route('/delete_push')
@requires_auth
def del_push():
    conn = sqlite3.connect("main.db")
    cursor = conn.execute("DELETE FROM QUESTIONS_Pushed")
    conn.commit()
    conn.close()
    return render_template('delete_response.html', message="Deleted " + str(cursor.rowcount) + " rows.")

@app.route('/delete_unpush')
@requires_auth
def del_unpush():
    conn = sqlite3.connect("main.db")
    cursor = conn.execute("DELETE FROM QUESTIONS")
    conn.commit()
    conn.close()
    return render_template('delete_response.html', message="Deleted " + str(cursor.rowcount) + " rows.")

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)
