from config import get_db_connection
from flask import request
from utils.response_helper import error_response, success_response


def verify_otp_service():
    data = request.get_json() or {}
    email = data.get("email")
    otp = data.get("otp") or data.get("otp_code")
    if not email or not otp:
        return error_response("email and otp/otp_code are required", 400)

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("CALL login.verify_otp_sp(%s, %s, %s)", (email, otp, None))
        row = cur.fetchone()

        if row is None:
            result = {"message": "OTP verified"}
        elif isinstance(row, dict):
            first_key = next(iter(row), None)
            result = row[first_key] if first_key is not None else row
        else:
            result = row[0]

        conn.commit()
        message = "OTP verified"
        data_payload = result

        if isinstance(result, dict):
            message = result.get("message", message)
        else:
            data_payload = {"result": result}

        return success_response(message, 200, data_payload)
    except Exception as e:
        return error_response(str(e), 500)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
