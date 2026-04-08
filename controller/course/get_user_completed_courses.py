from flask import request, jsonify
from config import get_db_connection
import psycopg2.extras


def get_user_completed_courses():

    user_id = request.args.get("user_id")

    if not user_id:
        return {
            "status": "fail",
            "message": "user_id is required",
            "data": []
        }, 400

    conn = None
    cursor = None

    try:
        conn = get_db_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        # Stored Procedure (INOUT p_user_id, OUT result)
        cursor.execute(
            "CALL course.get_user_completed_courses(%s, %s);",
            (user_id, None)
        )

        row = cursor.fetchone()

        # Check if result is empty
        if not row or not row.get("result"):
            return {
                "status": "success",
                "message": "You have not completed any courses yet",
                "data": []
            }, 200

        return {
            "status": "success",
            "message": "User completed courses fetched successfully",
            "data": row["result"]
        }, 200

    except Exception as e:
        import traceback
        print(traceback.format_exc())

        return {
            "status": "error",
            "message": "Failed to fetch completed courses",
            "error": repr(e)
        }, 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()
