from flask import request, jsonify, Blueprint, session
from flask import current_app as app
from flask_pymongo import PyMongo
import json
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


# Database and PWD
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


class fun_users:

    def __init__(self):
        version = "0.1"
        return (version)

    def create_users(__info__):
        __return__ = {}
        # Check for user First before building a user
        try:
            __results__ = fun_users.query_users(__info__)
            if "None" not in __results__["usrid"]:
                __return__ = {'usrid': "{0} is already registered".format( __results__['usrid'])}
                return(__return__)
            else:
                if __info__["debugging"] >= 1:
                    print("{0} need to be created - Lets work on that.".format(__info__['usrid']))
        except:
            if __info__["debugging"] >= 1:
                print("{0}".format('There was an error in the create user pre-user validation function'))
            __return__ = {"Error": "There was an error in the create user pre-user validation function"}
            return (__return__)
        # Create User
        try:
            db = mongo.cx[app.config["MONGO_DBNAME_2"]]
            users = db.users
            first_name = __info__['first_name']
            last_name = __info__['last_name']
            email = __info__['email']
            usrid = __info__['usrid']
            password = bcrypt.generate_password_hash(__info__['password']).decode('utf-8')
            created = datetime.utcnow()
            try:
                if __info__["debugging"] >= 1:
                    print("{0}".format('Inserting - Now'))
                user_id = users.insert({
                    'usrid': usrid,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'password': password,
                    'created': created
                })
            except:
                if __info__["debugging"] >= 1:
                    print("{0}".format('Error Inserting new record for user'))
                pass
            if __info__["debugging"] >= 1:
                print("{0}".format('Checking Post Insert - Now'))
            new_user = users.find_one({'_id': user_id})
            __return__ = {'usrid': new_user['email'] + ' registered'}
        except:
            __return__ = {'usrid': new_user['login'] + ' NOT registered',
                          'Error': "There was an error in creating the new user"}
        return (__return__)

    def query_users(__info__):
        __return__ = {}
        try:
            db = mongo.cx[app.config["MONGO_DBNAME_2"]]
            users = db.users
            login = __info__['usrid']
            __results__ = users.find_one({"usrid": login})
            if __results__ is None:
                __return__ = {
                    "usrid": "None",
                    'first_name': "None",
                    'last_name': "None",
                    'email': "None",
                    'privilege_level': 0,
                }
            else:
                for x in __results__:
                    try:
                        # String is required because the Mongo ID is an object return.
                        __return__[x] = str(__results__[x])
                    except:
                        pass
            '''
            __return__ = {
                "usrid": __user_return__["usrid"],
                'first_name': __user_return__["first_name"],
                'last_name': __user_return__["last_name"],
                'email': __user_return__["email"],
                'privilege_level': 1,
            }
            '''
        except:
            __return__ = {
                "usrid": "None",
                'first_name': "None",
                'last_name': "None",
                'email': "None",
                'privilege_level': 0,
            }
            if __info__["debugging"] >= 1:
                print('Failed to find the user {0}'.format(__info__)['login'])
        return (__return__)

    def remove_user(__info__):
        __return__ = {}
        # Check for user First before building a user
        try:
            print("{0}".format(__info__))
            __results__ = fun_users.query_users(__info__)
            if __info__["debugging"] >= 1:
                print("__results__ = {0}".format(__results__))
            if "None" in __results__["usrid"]:
                __return__ = {"usrid": "{0} Is not current a User.".format(__info__["usrid"])}
                return(__return__)
        except:
            __return__ = {"Error": "Error with the search for user function"}
            return (__return__)
        # Delete Record
        try:
            db = mongo.cx[app.config["MONGO_DBNAME_2"]]
            users = db.users
            if __info__["debugging"] >= 1:
                print("results = {0}".format(__results__))
            __results__ = users.delete_one({'_id': ObjectId(__results__['_id'])})
            if __info__["debugging"] >= 1:
                print("-----------------------")
                print("results = {0}".format(__results__))
                print("-----------------------")
                print("Deleted count =  {0}".format(__results__.deleted_count))
            if __results__.deleted_count <= 1 :
                __return__ = {"usrid": "{0} was removed.".format(__info__["usrid"])}
        except:
            if __info__["debugging"] >= 1:
                print("error deleting keep testing")
            __return__ = {"usrid": "{0} was NOT removed - error in function.".format(__info__["usrid"])}
            pass
        return(__return__)

    def update_users(__info__):
        __return__ = {}
        # Check for user First before building a user
        try:
            db = mongo.cx[app.config["MONGO_DBNAME_2"]]
            users = db.users
            __results__ = fun_users.query_users(__info__)
            if "None" in __results__["usrid"]:
                __return__ = {'usrid': __info__['usrid'] + ' is not found the the DB'}
                return(__return__)
            else:
                if __info__["debugging"] >= 1:
                    print("{0} is found and read for update.".format(__info__['usrid']))
        except:
            if __info__["debugging"] >= 1:
                print("{0}".format('There was an error in the update user pre-user validation function'))
            __return__ = {"Error": "There was an error in the update user pre-user validation function"}
            return (__return__)
        try:
            # Update Elements
            __id__ = __results__['_id']
            __debugging__ = 1
            __results__.update(__info__)
            # remove extra's
            __results__.pop("debugging")
            __results__.pop("_id")
            # Test and Update Passwords
            if __results__["password"]:
                new_password = bcrypt.generate_password_hash(__results__['password']).decode('utf-8')
                __results__['password'] = new_password
            user_id = users.update_one({"_id": ObjectId(__id__)}, {"$set": __results__})
            __return__ = {"usrid": "update status = {0}".format(user_id.acknowledged)}
        except:
            __return__ = {'usrid': __info__['usrid'] + ' was NOT updated',
                          'Error': "There was an error in updating the user"}
        return(__return__)

    def login_users(__info__):
        __return__ = {}
        try:
            db = mongo.cx[app.config["MONGO_DBNAME_2"]]
            users = db.users
            login = __info__['usrid']
            password = __info__['password']
            __return__ = {}
            response = users.find_one({'usrid': login})
            if response:
                if bcrypt.check_password_hash(response['password'], password):
                    expires = timedelta(minutes=30)
                    access_token = create_access_token(identity={
                        'email': response['email'],
                        'iat': datetime.utcnow(),  # Issue date
                        "exp": datetime.utcnow() + timedelta(minutes=30),  # DO NOT CHANGE THIS POSITION-VUE_isValidJwT
                        'usrid': response['usrid'],
                    }, expires_delta=expires)
                    __return__['access_token'] = access_token
                    __return__["status"] = "Logged in"
                else:
                    __return__['token'] = "Invalid username and password"
                    __return__["status"] = "Invalid username and password"
            else:
                __return__['token'] = "No user found"
                __return__["status"] = "No user found"
        except:
            __return__['Error'] = "There was a function error at {0}".format("login")
        return(__return__)
