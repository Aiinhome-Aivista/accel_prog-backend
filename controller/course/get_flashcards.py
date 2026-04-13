# from flask import request, jsonify
# from config import get_db_connection
# import psycopg2.extras


# def get_flashcards():

#     conn = None
#     cursor = None

#     try:
#         conn = get_db_connection()

#         cursor = conn.cursor(
#             cursor_factory=psycopg2.extras.RealDictCursor
#         )

#         # Calling stored procedure
#         cursor.execute(
#             "CALL login.get_flashcards(%s);",
#             (None,)
#         )

#         row = cursor.fetchone()

#         if not row or not row.get("result"):
#             return {
#                 "status": "fail",
#                 "message": "No response from stored procedure",
#                 "data": {}
#             }, 200

#         # Return EXACT stored procedure response
#         return row["result"], 200

#     except Exception as e:
#         import traceback
#         print(traceback.format_exc())

#         return {
#             "status": "error",
#             "message": "Failed to fetch flashcards",
#             "error": repr(e)
#         }, 500

#     finally:
#         if cursor:
#             cursor.close()

#         if conn:
#             conn.close()



from flask import request, jsonify
from config import get_db_connection
import psycopg2.extras
from utils.logging_service import log_api   #import add


@log_api("get-flashcards")   # decorator add
def get_flashcards():

    conn = None
    cursor = None

    try:
        conn = get_db_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        # Calling stored procedure
        cursor.execute(
            "CALL login.get_flashcards(%s);",
            (None,)
        )

        row = cursor.fetchone()

        if not row or not row.get("result"):
            return {
                "status": "fail",
                "message": "No response from stored procedure",
                "data": {}
            }, 200

        # Return EXACT stored procedure response
        return row["result"], 200

    except Exception as e:
        import traceback
        print(traceback.format_exc())

        return {
            "status": "error",
            "message": "Failed to fetch flashcards",
            "error": repr(e)
        }, 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()