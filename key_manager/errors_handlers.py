from flask import jsonify, request


def handle_bad_request(e):
    """"""
    return jsonify(success=False, msg="Bad Request {}!".format(request.url)), 400


def handle_not_found_request(e):
    """"""
    return jsonify(success=False, msg="Resource {} not found!".format(request.url)), 404


def handle_internal_server_error_request(e):
    """"""
    return jsonify(success=False, msg="An Error has occurred! Please try again later."), 404


def handle_validation_error(e):
    return jsonify(e.messages), 400


def handle_database_error(e):
    return str(e), 400