from config import get_db_connection
from flask import jsonify, request


def get_modules_dashboard_service():
    data = request.get_json() or {}

    course_id = data.get("course_id")
    if not course_id:
        return jsonify({"status": "error", "message": "course_id is required"}), 400

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # CALL procedure
        cur.execute("CALL course.get_modules_with_days(%s, %s)", (course_id, None))

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
