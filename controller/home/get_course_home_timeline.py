from flask import request
from config import get_db_connection
import psycopg2.extras


def get_course_home_timeline():
    data = request.json
    course_id = data.get("course_id")
    user_id = data.get("user_id")

    # validation
    if not course_id or not user_id:
        return {"status": "error", "message": "course_id and user_id are required"}, 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # ✅ CALL procedure
        cursor.execute(
            "CALL course.get_course_home_timeline(%s::INT, %s::BIGINT, %s::JSONB);",
            (course_id, user_id, None),
        )

        row = cursor.fetchone()

        # empty response handle
        if not row or not row.get("result"):
            return {"status": "error", "message": "No response from procedure"}, 500

        return {"status": "success", "data": row["result"]}, 200

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

    finally:
        cursor.close()
        conn.close()
