# from flask import jsonify
# from config import get_db_connection
# import psycopg2.extras


# def get_master_dropdown_data():
#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

#     try:
#         # 🔹 CALL procedure
#         cursor.execute(
#             "CALL course.get_master_dropdown_data_v1(%s::JSONB);",
#             (None,)
#         )

#         row = cursor.fetchone()

#         # 🔹 empty response handle
#         if not row or not row.get("p_result"):
#             return jsonify({
#                 "status": "error",
#                 "message": "No data found"
#             }), 500

#         return jsonify({
#             "status": "success",
#             "data": row["p_result"]
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

#     finally:
#         cursor.close()
#         conn.close()




from flask import jsonify
from config import get_db_connection
import psycopg2.extras
from utils.logging_service import log_api   # import add


@log_api("get_master_dropdown_data")   # decorator add
def get_master_dropdown_data():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # 🔹 CALL procedure
        cursor.execute(
            "CALL course.get_master_dropdown_data_v1(%s::JSONB);",
            (None,)
        )

        row = cursor.fetchone()

        # 🔹 empty response handle
        if not row or not row.get("p_result"):
            return jsonify({
                "status": "error",
                "message": "No data found"
            }), 500

        return jsonify({
            "status": "success",
            "data": row["p_result"]
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()