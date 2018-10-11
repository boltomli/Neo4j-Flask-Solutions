#!/usr/bin/env python

# -*- coding: utf-8 -*-

from flask import Flask
from flask_restplus import Api, Resource

from models import graph, query_on_constraint, list_all

# Settings
DEBUG = False

# Application, RESTful API and namespace
APP = Flask(__name__)
APP.config.from_object(__name__)
API = Api(APP, version='1.0', title='Query API', doc='/api',
          description='Query info.')
NS = API.namespace('query')

# API
@NS.route('/view/<string:constraint>')
class View(Resource):
    def get(self, constraint):
        return query_on_constraint(constraint)

@NS.route('/list')
class List(Resource):
    def get(self):
        return list_all()

if __name__ == '__main__':
    graph.schema.create_uniqueness_constraint('Label', 'Constraint')
    APP.run(host='0.0.0.0', debug=DEBUG)
