import os
import logging
from flask import Flask
from flask import send_from_directory
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

from controller.get_user_enrolled_courses import get_user_enrolled_courses
from controller.course.get_user_completed_courses import get_user_completed_courses

from controller.course.get_dashboard_kpi_by_user import get_dashboard_kpi_by_user

from controller.course.enroll_user import enroll_user
from controller.course.get_grades_info_by_user import get_grades_info_by_user_service
from controller.course.get_user_recent_activity import get_user_recent_activity
from controller.admin.admin_generate_otp import admin_generate_otp
from controller.admin.admin_verify_otp import admin_verify_otp
from controller.course.get_flashcards import get_flashcards
from controller.course.get_master_dropdown_data import get_master_dropdown_data
from controller.course.save_content import save_content
from controller.course.get_course_learning_content_by_user import get_course_learning_content_by_user

from controller.course.get_course_videos import get_course_videos
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

@app.route(BASE_URL + "get-enrolled-courses-by-user-id", methods=["GET"])
def get_user_enrolled_courses_route():  
    return get_user_enrolled_courses()

@app.route(BASE_URL + "get-completed-courses-by-user-id", methods=["GET"])
def get_user_completed_courses_route():
    return get_user_completed_courses()

@app.route(BASE_URL + "get_courses_dashboard", methods=["GET"])
def get_courses_dashboard_route():
    return get_courses_dashboard_service()

@app.route(BASE_URL + "dashboard_kpi_by_user", methods=["POST"])
def get_dashboard_kpi_by_user_route():
    return get_dashboard_kpi_by_user()


@app.route(BASE_URL + "get_modules_dashboard", methods=["POST"])
def get_modules_dashboard():
    return get_modules_dashboard_service()

@app.route(BASE_URL + "course_enrollment", methods=["POST"])
def enroll_user_route():
    return enroll_user()

@app.route(BASE_URL + "grades_info_by_user", methods=["GET"])
def get_grades_info_by_user_route():
    return get_grades_info_by_user_service()

@app.route(BASE_URL + "get-user-recent-activity", methods=["GET"])
def get_user_recent_activity_route():
    return get_user_recent_activity()

@app.route(BASE_URL + "get-flashcards", methods=["GET"])
def get_flashcards_route():
    return get_flashcards()


@app.route(BASE_URL + "admin_generate_otp", methods=["POST"])
def admin_generate_otp_route(): 
    return admin_generate_otp()

@app.route(BASE_URL + "admin_verify_otp", methods=["POST"])
def admin_verify_otp_route():   
    return admin_verify_otp()

@app.route(BASE_URL + "get_master_dropdown_data", methods=["GET"])
def get_master_dropdown_data_route():
    return get_master_dropdown_data()

@app.route(BASE_URL + "save_content", methods=["POST"])
def save_content_route():   
    return save_content()

@app.route(BASE_URL + "get_course_learning_content_by_user", methods=["POST"])  
def get_course_learning_content_by_user_route():
    return get_course_learning_content_by_user()  

@app.route(BASE_URL + "get_course_videos", methods=["GET"])
def get_course_videos_route():
    return get_course_videos() 

@app.route("/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory("static/videos", filename) 

def check_db_connection():
    conn = None


if __name__ == "__main__":
    check_db_connection()
    port = int(os.environ.get("PORT", 8000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    print(f"Server running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
