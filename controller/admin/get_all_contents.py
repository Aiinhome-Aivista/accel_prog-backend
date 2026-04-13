# from flask import request
# from config import get_db_connection
# import psycopg2.extras

# def get_all_contents():
#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

#     try:
#         cursor.execute(
#             "CALL course.get_all_contents(%s);",
#             (None,)
#         )

#         row = cursor.fetchone()

#         if not row or not row.get("p_result"):
#             return {
#                 "status": "error",
#                 "message": "No data found"
#             }, 500

#         return row["p_result"], 200

#     except Exception as e:
#         return {
#             "status": "error",
#             "message": str(e)
#         }, 500

#     finally:
#         cursor.close()
#         conn.close()



from flask import request
from config import get_db_connection
import psycopg2.extras
from utils.logging_service import log_api


@log_api("admin/get_all_contents")
def get_all_contents():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute(
            "CALL course.get_all_contents(%s);",
            (None,)
        )

        row = cursor.fetchone()

        if not row or not row.get("p_result"):
            return {
                "status": "error",
                "message": "No data found"
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