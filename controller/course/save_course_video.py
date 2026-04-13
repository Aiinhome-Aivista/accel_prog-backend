import os
from flask import request, jsonify
from config import get_db_connection
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "static/videos"
DB_PATH_PREFIX = "/videos"


def save_course_video():

    course_id = request.form.get("course_id")
    module_id = request.form.get("module_id")
    subtopic_id = request.form.get("subtopic_id")
    video_title = request.form.get("video_title")
    video_subtitle = request.form.get("video_subtitle")
    is_intro_video = request.form.get("is_intro_video")
    user_id = request.form.get("user_id")

    file = request.files.get("video")

    # Validation
    if not all([
        course_id,
        module_id,
        subtopic_id,
        video_title,
        user_id,
        file
    ]):
        return jsonify({
            "status": "error",
            "message": "course_id, module_id, subtopic_id, video_title, user_id and video file are required"
        }), 400

    conn = None
    cur = None

    try:

        # Ensure folder exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Keep original filename
        filename = secure_filename(file.filename)

        # Actual file save path
        file_save_path = f"{UPLOAD_FOLDER}/{filename}"

        # DB path (what frontend uses)
        db_video_path = f"{DB_PATH_PREFIX}/{filename}"

        # Save file
        file.save(file_save_path)

        # DB connection
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "CALL course.save_course_video(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                course_id,
                module_id,
                subtopic_id,
                video_title,
                video_subtitle,
                db_video_path,
                is_intro_video,
                user_id,
                None
            )
        )

        row = cur.fetchone()

        if row is None:
            result = {"message": "Video uploaded successfully"}

        elif isinstance(row, dict):
            first_key = next(iter(row), None)
            result = row[first_key] if first_key else row

        else:
            result = row[0]

        conn.commit()

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()
