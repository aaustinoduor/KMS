from flask import jsonify, request


def handle_bad_request(e):
    """"""
    return jsonify(msg="Bad Request {}!".format(request.url), success=False), 400


def handle_not_found_request(e):
    """"""
    return jsonify(msg="Resource {} not found!".format(request.url), success=False), 404


def handle_internal_server_error_request(e):
    """"""
    return jsonify(msg="An Error has occurred! Please try again later.", success=False), 500


def handle_validation_error(e):
    return jsonify(errors=e.messages, success=False), 400


def handle_database_error(e):
    return jsonify(msg="Database error", success=False), 500