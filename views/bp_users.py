from flask import request, jsonify, Blueprint, session
from flask import current_app as app
from flask_pymongo import PyMongo
import json
from bson.objectid import ObjectId
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_current_user
# Import supporting models
from models.fun_users import fun_users

# User Blueprint List
bp_users = Blueprint("users", __name__, url_prefix="/users")

# Database and PWD
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


'''  API - Routes '''

@bp_users.route('/test', methods=['GET', 'POST'])
def url_login_test():
    return jsonify({"message:": "Test successful"})

@bp_users.route('/register', methods=['POST'])
def register():
    __info__ = request.get_json()
    __results__ = fun_users.create_users(__info__)
    return jsonify({'result': __results__})

@bp_users.route('/login', methods=['POST'])
def login():
    __info__ = request.get_json()
    __results__ = fun_users.login_users(__info__)
    return jsonify({'result': __results__})



# @bp_users.route('/<userid>', methods=['GET'])
# @jwt_required
# def queryuser(userid):
#     __info__ = request.get_json()
#     __info__['usrid'] = userid
#     __results__ = fun_users.query_users(__info__)
#     return jsonify({'result': __results__})
#
#
# @bp_users.route('/<userid>', methods=['POST'])
# @jwt_required
# def updateuser(userid):
#     __info__ = request.get_json()
#     __info__['usrid'] = userid
#     __results__ = fun_users.update_users(__info__)
#     return jsonify({'result': __results__})
#
#
# @bp_users.route('/<userid>', methods=['DELETE'])
# @jwt_required
# def removeuser(userid):
#     print("The current user is {0}".format(get_current_user()))
#     __info__ = request.get_json()
#     __info__['usrid'] = userid
#     __results__ = fun_users.remove_user(__info__)
#     return jsonify({'result': __results__})


class users(Resource):
    @bp_users.route('/<userid>',)
@jwt_required
def queryuser(userid):
    __info__ = request.get_json()
    __info__['usrid'] = userid
    __results__ = fun_users.query_users(__info__)
    return jsonify({'result': __results__})


@bp_users.route('/<userid>', methods=['POST'])
@jwt_required
def updateuser(userid):
    __info__ = request.get_json()
    __info__['usrid'] = userid
    __results__ = fun_users.update_users(__info__)
    return jsonify({'result': __results__})


@bp_users.route('/<userid>', methods=['DELETE'])
@jwt_required
def removeuser(userid):
    print("The current user is {0}".format(get_current_user()))
    __info__ = request.get_json()
    __info__['usrid'] = userid
    __results__ = fun_users.remove_user(__info__)
    return jsonify({'result': __results__})