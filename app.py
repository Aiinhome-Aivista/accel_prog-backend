import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import get_db_connection
from controller.course_controller import (
    create_course,
    get_courses,
    get_course_details,
)
from controller.module_controller import add_module
from controller.capstone_controller import add_capstone
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "/api/v1/"


@app.route("/")
def health():
    return "API is running"


@app.route(BASE_URL + "courses", methods=["POST"])
def create_course_route():
    return create_course()


@app.route(BASE_URL + "courses", methods=["GET"])
def get_courses_route():
    return get_courses()


@app.route(BASE_URL + "courses/<int:course_id>", methods=["GET"])
def get_course_details_route(course_id):
    return get_course_details(course_id)


@app.route(BASE_URL + "modules", methods=["POST"])
def add_module_route():
    return add_module()


@app.route(BASE_URL + "capstones", methods=["POST"])
def add_capstone_route():
    return add_capstone()


def check_db_connection():
    conn = None


if __name__ == "__main__":
    check_db_connection()
    port = int(os.environ.get("PORT", 8000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    print(f"Server running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
