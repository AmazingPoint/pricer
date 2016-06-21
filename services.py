#-*- coding:utf8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from price import Pricer

from flask import Flask,request,jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    good_name = request.args.get('gname')
    print good_name
    pricer = Pricer(good_name)
    pricer.price_run()
    dic = pricer.response()
    return jsonify(**dic)

if __name__ == '__main__':
    app.run()
