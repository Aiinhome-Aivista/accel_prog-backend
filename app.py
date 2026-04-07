import os
import logging
from flask import Flask
from flask_cors import CORS
from controller.course.get_courses import get_program_courses
from controller.course.capstone_controller import add_capstone
import sys
from controller.course.get_courses_dashboard_service import (
    get_courses_dashboard_service,
)
from controller.course.get_modules import get_modules_dashboard_service
from controller.login_registration.login import login
from controller.otp.send_otp import send_otp_service
from controller.otp.verify_otp import verify_otp_service
from controller.login_registration.registration import register
from controller.login_registration.google_signin import google_signin

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "/api/v1/"


@app.route("/")
def health():
    return "API is running"


# @app.route(BASE_URL + "courses", methods=["POST"])
# def create_course_route():
#     return create_course()


@app.route(BASE_URL + "courses", methods=["GET"])
def get_program_courses_route():
    return get_program_courses()


@app.route(BASE_URL + "login", methods=["POST"])
def login_route():
    return login()


@app.route(BASE_URL + "send-otp", methods=["POST"])
def send_otp_route():
    return send_otp_service()


@app.route(BASE_URL + "verify-otp", methods=["POST"])
def verify_otp_route():
    return verify_otp_service()


@app.route(BASE_URL + "google-signin", methods=["POST"])
def google_signin_route():
    return google_signin()


# @app.route(BASE_URL + "courses/<int:course_id>", methods=["GET"])
# def get_course_details_route(course_id):
#     return get_course_details(course_id)


# @app.route(BASE_URL + "modules", methods=["POST"])
# def add_module_route():
#     return add_module()


@app.route(BASE_URL + "capstones", methods=["POST"])
def add_capstone_route():
    return add_capstone()


@app.route(BASE_URL + "register", methods=["POST"])
def register_route():
    return register()


@app.route(BASE_URL + "get_courses_dashboard", methods=["GET"])
def get_courses_dashboard_route():
    return get_courses_dashboard_service()


@app.route(BASE_URL + "get_modules_dashboard", methods=["POST"])
def get_modules_dashboard():
    return get_modules_dashboard_service()


def check_db_connection():
    conn = None


if __name__ == "__main__":
    check_db_connection()
    port = int(os.environ.get("PORT", 8000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    print(f"Server running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
