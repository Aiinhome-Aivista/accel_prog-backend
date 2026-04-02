from config import get_db_connection
from flask import request, jsonify


def create_course():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL usp_create_course(%s, %s, %s, %s)",
        (
            data["course_name"],
            data.get("course_level"),
            data.get("tagline"),
            data.get("description"),
        ),
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Course created successfully"})


def get_courses():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM usp_get_courses()")
    result = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(result)


def get_course_details(course_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT usp_get_course_details(%s)", (course_id,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify(result["usp_get_course_details"])
