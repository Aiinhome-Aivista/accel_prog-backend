from flask import jsonify
from config import get_db_connection


def get_all_course_video_mapping():

    conn = None
    cur = None

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "CALL course.get_all_course_video_mapping(%s)",
            (None,)
        )

        row = cur.fetchone()

        if row is None:
            result = {}
        elif isinstance(row, dict):
            first_key = next(iter(row), None)
            result = row[first_key] if first_key else row
        else:
            result = row[0]

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()
