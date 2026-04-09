from config import get_db_connection
from flask import jsonify, request


def get_course_videos():

    course_id = request.args.get("course_id")

    if not course_id:
        return jsonify({
            "error": "course_id is required"
        }), 400

    conn = None
    cur = None

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "CALL course.get_course_videos(%s,%s)",
            (course_id, None)
        )

        row = cur.fetchone()

        if row is None:
            result = {"message": "No video data found"}

        elif isinstance(row, dict):
            first_key = next(iter(row), None)
            result = row[first_key] if first_key else row

        else:
            result = row[0]

        # ADD THIS BLOCK
        base_url = request.host_url.rstrip("/")

        if result.get("course_intro_video"):

            result["course_intro_video"]["video_path"] = \
                base_url + result["course_intro_video"]["video_path"]

        if result.get("week_videos"):

            for video in result["week_videos"]:

                video["video_path"] = base_url + video["video_path"]

        conn.commit()

        return jsonify(result), 200

    except Exception as e:

        return jsonify({"error": str(e)}), 500

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()
