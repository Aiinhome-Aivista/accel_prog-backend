# from config import get_db_connection
# from flask import request, jsonify


# def add_module():
#     data = request.json
#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute(
#         "CALL usp_add_module(%s, %s, %s, %s)",
#         (
#             data["course_id"],
#             data["module_name"],
#             data.get("module_description"),
#             data.get("module_order"),
#         ),
#     )

#     conn.commit()
#     cur.close()
#     conn.close()

#     return jsonify({"message": "Module added"})



from config import get_db_connection
from flask import request, jsonify
from utils.logging_service import log_api   # ✅ import add


@log_api("add-module")   # ✅ decorator add
def add_module():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL usp_add_module(%s, %s, %s, %s)",
            (
                data["course_id"],
                data["module_name"],
                data.get("module_description"),
                data.get("module_order"),
            ),
        )

        conn.commit()

        return jsonify({"message": "Module added"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        cur.close()
        conn.close()