from flask import request
from config import get_db_connection
import psycopg2.extras


def admin_generate_otp():
    data = request.json
    email = data.get("email")

    if not email:
        return {
            "status": "error",
            "message": "Email is required"
        }, 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # 🔹 CALL procedure (same pattern as your grades API)
        cursor.execute(
            "CALL admin.admin_generate_otp(%s::VARCHAR, %s::JSONB);",
            (email, None)
        )

        row = cursor.fetchone()

        # 🔹 empty handle
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