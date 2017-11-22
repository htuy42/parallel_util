import json
import sys
import uuid

import flask
from flask import Flask
from flask_rest_toolkit.api import Api
from flask_rest_toolkit.endpoint import ApiEndpoint
from flask import request, jsonify

from parents import ControlParent
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask("ga")


app.secret_key = "dog"

print("start")

par = ControlParent.ControlParent(sys.argv[1:],len(sys.argv) - 1)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/ga/register', methods=['POST'])
def register():
    ida = str(uuid.uuid4())
    r = par.add_child(ida)
    return jsonify(r)


@app.route('/ga/instr', methods=['POST'])
def instruct():
    if request.method == 'POST':
        k = par.request_instruction(request.form['id'])
        return jsonify(k)

@app.route('/ga/report', methods=['POST'])
def report():
    if request.method == 'POST':
        return jsonify(par.report_result(request.form['id'],request.form['res']))


@app.route('/ga/kill', methods=['POST'])
def unregister():
    if request.method == 'POST':
        par.unregister(request.form['id'])
        return jsonify({'status':200})


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run()
    app.log_exception("running")
    print("running")
