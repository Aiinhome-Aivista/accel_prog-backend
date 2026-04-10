import os
from flask import request, jsonify
from config import get_db_connection
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "projects"


def upload_project():

    user_id = request.form.get("user_id")
    course_id = request.form.get("course_id")
    module_id = request.form.get("module_id")
    subtopic_id = request.form.get("subtopic_id")

    file = request.files.get("file")

    if not user_id or not course_id or not module_id or not subtopic_id or not file:

        return jsonify({
            "error": "user_id, course_id, module_id, subtopic_id and file are required"
        }), 400

    conn = None
    cur = None

    try:

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        original_filename = secure_filename(file.filename)

        file_base_name = os.path.splitext(original_filename)[0]
        file_extension = os.path.splitext(original_filename)[1]

        filename = f"{file_base_name}_{user_id}{file_extension}"

        file_path = f"{UPLOAD_FOLDER}/{filename}"

        file.save(file_path)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "CALL course.save_project_submission(%s,%s,%s,%s,%s,%s)",
            (
                user_id,
                course_id,
                module_id,
                subtopic_id,
                file_path,
                None
            )
        )

        row = cur.fetchone()

        if row is None:
            result = {"message": "Project uploaded"}
        elif isinstance(row, dict):
            first_key = next(iter(row), None)
            result = row[first_key] if first_key else row
        else:
            result = row[0]

        conn.commit()

        return jsonify(result), 200

    except Exception as e:

        return jsonify({"error": str(e)}), 500

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()
