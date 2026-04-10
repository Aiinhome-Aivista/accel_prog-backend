from flask import request, jsonify
from config import get_db_connection


def save_course_video():

    data = request.get_json() or {}

    course_id = data.get("course_id")
    module_id = data.get("module_id")
    subtopic_id = data.get("subtopic_id")
    video_title = data.get("video_title")
    video_subtitle = data.get("video_subtitle")
    video_path = data.get("video_path")
    is_intro_video = data.get("is_intro_video")
    user_id = data.get("user_id")

    # Validation block to check if all required fields are present
    if not all([
        course_id,
        module_id,
        subtopic_id,
        video_title,
        video_path,
        user_id
    ]):
        return jsonify({
            "status": "error",
            "message": "All fields are required"
        }), 400

    conn = None
    cur = None

    try:

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
                video_path,
                is_intro_video,
                user_id,
                None
            )
        )

        row = cur.fetchone()

        if row is None:
            result = {
                "status": "error",
                "message": "No response from database"
            }

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
