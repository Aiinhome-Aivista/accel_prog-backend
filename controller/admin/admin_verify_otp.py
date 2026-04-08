from flask import request
from config import get_db_connection
import psycopg2.extras


def admin_verify_otp():
    data = request.json
    email = data.get("email")
    otp_code = data.get("otp_code")

    #  validation
    if not email or not otp_code:
        return {
            "status": "error",
            "message": "Email and OTP are required"
        }, 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        #  CALL procedure
        cursor.execute(
            "CALL admin.admin_verify_otp(%s::VARCHAR, %s::VARCHAR, %s::JSONB);",
            (email, otp_code, None)
        )

        row = cursor.fetchone()

        #  empty response handle
        if not row or not row.get("p_result"):
            return {
                "status": "error",
                "message": "No response from procedure"
            }, 500

        return row["p_result"], 200

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500

    finally:
        cursor.close()
        conn.close()