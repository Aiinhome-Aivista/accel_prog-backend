# from config import get_db_connection
# from flask import request, jsonify


# def add_capstone():
#     data = request.json
#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute(
#         "CALL usp_add_capstone(%s, %s, %s)",
#         (data["course_id"], data["title"], data.get("description")),
#     )

#     conn.commit()
#     cur.close()
#     conn.close()

#     return jsonify({"message": "Capstone added"})



from config import get_db_connection
from flask import request, jsonify
from utils.logging_service import log_api   # import add


@log_api("capstones")   # decorator add
def add_capstone():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL usp_add_capstone(%s, %s, %s)",
        (data["course_id"], data["title"], data.get("description")),
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Capstone added"})