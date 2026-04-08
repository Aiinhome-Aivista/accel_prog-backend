from flask import request
from config import get_db_connection
import psycopg2.extras


def get_grades_info_by_user_service():

    user_id = request.args.get("user_id", type=int)

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
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(
            "CALL login.get_grades_info_by_user(%s::BIGINT, %s::JSONB);",
            (user_id, None)
        )

        row = cursor.fetchone()

        #  empty handle
        if not row or not row.get("p_result"):
            return {
                "status": "success",
                "message": "No data found",
                "data": {}
            }, 200

        return {
            "status": "success",
            "message": "Grades info fetched successfully",
            "data": row["p_result"]
        }, 200

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {
            "status": "error",
            "message": "Failed to fetch grades info",
            "error": repr(e)
        }, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()