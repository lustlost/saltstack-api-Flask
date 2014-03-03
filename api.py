# -*- coding: utf-8 -*- 

from flask import Flask
from flask.ext import restful
from apimodules import saltApi

app = Flask(__name__)
api = restful.Api(app)
api.add_resource(saltApi,'/api')


#app.debug = True
#app.run(host='0.0.0.0')
