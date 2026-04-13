# from flask import request
# from config import get_db_connection
# import psycopg2.extras


# def get_course_learning_content_by_user():
#     data = request.json

#     user_id = data.get("user_id")
#     course_id = data.get("course_id")

#     #  validation
#     if not user_id or not course_id:
#         return {
#             "status": "error",
#             "message": "user_id and course_id are required"
#         }, 400

#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

#     try:
#         #  CALL procedure
#         cursor.execute(
#             "CALL course.get_course_learning_content_by_user(%s, %s, %s);",
#             (user_id, course_id, None)
#         )

#         row = cursor.fetchone()

#         #  no response handle
#         if not row or not row.get("p_result"):
#             return {
#                 "status": "error",
#                 "message": "No response from procedure"
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
from utils.logging_service import log_api   # import add


@log_api("get_course_learning_content_by_user")   # decorator add
def get_course_learning_content_by_user():
    data = request.json or {}

    user_id = data.get("user_id")
    course_id = data.get("course_id")

    #  validation
    if not user_id or not course_id:
        return {
            "status": "error",
            "message": "user_id and course_id are required"
        }, 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        #  CALL procedure
        cursor.execute(
            "CALL course.get_course_learning_content_by_user(%s, %s, %s);",
            (user_id, course_id, None)
        )

        row = cursor.fetchone()

        #  no response handle
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