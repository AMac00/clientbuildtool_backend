from flask import Blueprint, request, jsonify, session, current_app

# Dev URL List

bp_dev = Blueprint("url_dev", "url_dev", url_prefix="/dev")

@bp_dev.route('/test', methods=['GET', 'POST'])
def url_dev_test():
    return jsonify(current_app.config["MONGO_SERVER"])

@bp_dev.route('/<unbuilt>', methods=['GET', 'POST'])
def url_dev_unbuilt(unbuilt):
    return jsonify({"message:": "Test successful {0}".format(unbuilt)})