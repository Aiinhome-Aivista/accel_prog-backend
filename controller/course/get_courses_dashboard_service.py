from config import get_db_connection
from flask import jsonify


def get_courses_dashboard_service():
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # CALL procedure (same style as OTP)
        cur.execute("CALL course.get_all_courses_dashboard(%s)", (None,))

        row = cur.fetchone()

        if row is None:
            result = []
        elif isinstance(row, dict):
            first_key = next(iter(row), None)
            result = row[first_key] if first_key is not None else row
        else:
            result = row[0]

        conn.commit()

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
