from config import get_db_connection


def add_capstone(data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL usp_add_capstone(%s, %s, %s)",
        (data["course_id"], data["title"], data.get("description")),
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Capstone added"}

