from flask import jsonify


def api_response(status, message, status_code, data=None):
    payload = {
        "status": status,
        "status_code": status_code,
        "message": message,
    }
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status_code


def success_response(message, status_code=200, data=None):
    return api_response("success", message, status_code, data)


def error_response(message, status_code=400, data=None):
    return api_response("error", message, status_code, data)
