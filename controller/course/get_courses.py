from flask import jsonify
from config import get_db_connection
from flask import jsonify
import psycopg2.extras

def get_program_courses():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()

        # ✅ dict-based cursor
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("SELECT course.fn_get_program_with_courses_wrapper() AS data;")

        row = cursor.fetchone()

        if not row or not row["data"]:
            return {
                "status": "fail",
                "message": "No program data found",
                "data": []
            }, 404

        return {
            "status": "success",
            "message": "Program courses fetched successfully",
            "data": row["data"]
        }, 200

    except Exception as e:
        import traceback
        print(traceback.format_exc())

        return {
            "status": "error",
            "message": "Failed to fetch program courses",
            "error": repr(e)
        }, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()