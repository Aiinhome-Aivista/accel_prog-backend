from flask import request, jsonify
from config import get_db_connection
import psycopg2.extras


def get_user_recent_activity():

    user_id = request.args.get("user_id")

    if not user_id:
        return {
            "status": "fail",
            "message": "user_id is required",
            "data": {}
        }, 400

    conn = None
    cursor = None

    try:
        conn = get_db_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        # Calling stored procedure
        cursor.execute(
            "CALL login.get_user_recent_activity_v2(%s, %s);",
            (user_id, None)
        )

        row = cursor.fetchone()

        # If SP returns nothing (rare case)
        if not row or not row.get("result"):
            return {
                "status": "success",
                "data": {}
            }, 200

        # Return EXACT stored procedure response
        return {
            "status": "success",
            "data": row["result"]
        }, 200

    except Exception as e:
        import traceback
        print(traceback.format_exc())

        return {
            "status": "error",
            "message": "Failed to fetch recent activity",
            "error": repr(e)
        }, 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()
