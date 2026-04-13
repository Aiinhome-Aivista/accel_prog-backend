from http.client import HTTPException
import os
import logging
from flask import Flask, jsonify, request
from flask import send_from_directory
from flask_cors import CORS
from controller.admin.manage_assesment import manage_assessment_questions
from controller.course.assessment_questions import get_assessment_questions_v2
from controller.course.get_courses import get_program_courses
from controller.course.capstone_controller import add_capstone
import sys
from controller.course.get_courses_dashboard_service import (
    get_courses_dashboard_service,
)
from logger_config import logger
from controller.course.get_modules import get_modules_dashboard_service
from controller.login_registration.login import login
from controller.otp.send_otp import send_otp_service
from controller.otp.verify_otp import verify_otp_service
from controller.login_registration.registration import register
from controller.login_registration.google_signin import google_signin

from controller.course.get_user_enrolled_courses import get_user_enrolled_courses
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
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from controller.course.get_course_videos import get_course_videos
from controller.home.get_course_home_overview import get_course_home_overview
from controller.home.get_course_home_timeline import get_course_home_timeline
from controller.admin.get_all_contents import get_all_contents
from controller.course.complete_subtopic_module_course_wise_by_user import complete_subtopic_module_course_wise_by_user
from controller.course.submit_user_answer import submit_user_answer
from controller.course.submit_cohort_answer import submit_cohort_answer
from controller.course.project_upload_by_user import upload_project
from controller.course.get_user_weekly_streak import get_user_weekly_streak 
from logger_config import logger
from controller.course.get_courses_dashboard_service import (
    get_courses_dashboard_service,
)
from controller.course.get_all_video_mapping import get_all_course_video_mapping
from controller.course.save_course_video import save_course_video
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
CORS(app)  # Enable CORS for frontend communication

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "/api/v1/"

####################
@app.after_request
def log_response(response):
    logger.info(
        "Outgoing response",
        extra={
            "custom_dimensions": {
                "status": response.status,
                "endpoint": request.endpoint
            }
        }
    )
    return response


# 🔹 Response logging
# @app.after_request
# def log_response(response):
#     logger.info(f"[RESPONSE] Status={response.status}")
#     return response

@app.after_request
def log_response(response):
    logger.info(
        "Outgoing response",
        extra={
            "custom_dimensions": {
                "status": response.status,
                "endpoint": request.endpoint
            }
        }
    )
    return response


# 🔹 Global error handler
# @app.errorhandler(Exception)
# def handle_exception(e):
#     logger.error("[APP ERROR]", exc_info=True)
#     return jsonify({
#         "status": "error",
#         "message": "Internal Server Error"
#     }), 500


# @app.errorhandler(Exception)
# def handle_exception(e):
#     logger.error(f"[APP ERROR] {str(e)}", exc_info=True)
#     return jsonify({
#         "status": "error",
#         "message": str(e)  # ✅ actual error 
#     }), 500


# @app.errorhandler(Exception)
# def handle_exception(e):
#     logger.exception(
#         "Unhandled Exception",
#         extra={
#             "custom_dimensions": {
#                 "endpoint": request.endpoint,
#                 "url": request.url
#             }
#         }
#     )
#     return jsonify({
#         "status": "error",
#         "message": str(e)
#     }), 500


# # ✅ HTTP Errors (400, 404, 405 etc.)
# @app.errorhandler(HTTPException)
# def handle_http_exception(e):
#     logger.error(
#         f"HTTP ERROR {e.code} - {e.name}",
#         extra={
#             "custom_dimensions": {
#                 "endpoint": request.endpoint,
#                 "url": request.url,
#                 "status_code": e.code,
#                 "error": e.description
#             }
#         }
#     )

#     return jsonify({
#         "status": "fail",
#         "message": e.description
#     }), e.code


# # ✅ General Exceptions (500 etc.)
# @app.errorhandler(Exception)
# def handle_exception(e):
#     logger.exception(
#         "Unhandled Exception",
#         extra={
#             "custom_dimensions": {
#                 "endpoint": request.endpoint,
#                 "url": request.url
#             }
#         }
#     )

#     return jsonify({
#         "status": "error",
#         "message": str(e)
#     }), 500


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    logger.error(
        f"HTTP ERROR {e.code} - {e.name}",
        extra={
            "custom_dimensions": {
                "type": "HTTP_ERROR",
                "endpoint": request.endpoint,
                "url": request.url,
                "method": request.method,
                "status_code": e.code,
                "error": e.description
            }
        }
    )

    return jsonify({
        "status": "fail",
        "message": e.description
    }), e.code


# (optional but recommended)
@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception(
        "UNHANDLED EXCEPTION",
        extra={
            "custom_dimensions": {
                "type": "SYSTEM_ERROR",
                "endpoint": request.endpoint,
                "url": request.url,
                "method": request.method,
                "error": str(e)
            }
        }
    )

    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500



##########################




###################




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


@app.route(BASE_URL + "course_home_overview", methods=["POST"])
def course_home_overview_route():
    return get_course_home_overview()


@app.route(BASE_URL + "course_home_timeline", methods=["POST"])
def course_home_timeline_route():
    return get_course_home_timeline()
    
@app.route(BASE_URL + "admin/get_all_contents", methods=["GET"])
def get_all_contents_route():
    return get_all_contents()

@app.route(BASE_URL + "complete_subtopic_module_course_wise_by_user", methods=["POST"])
def complete_subtopic_module_course_wise_by_user_route():
    return complete_subtopic_module_course_wise_by_user()

@app.route(BASE_URL + "submit_user_answer", methods=["POST"])
def submit_user_answer_route():
    return submit_user_answer()

@app.route(BASE_URL + "submit_cohort_answer", methods=["POST"])
def submit_cohort_answer_route():
    return submit_cohort_answer()
@app.route(BASE_URL + "get-assessment-questions", methods=["GET"])
def get_assessment_questions_route():
    return get_assessment_questions_v2()


@app.route(BASE_URL + "manage-assessment-questions", methods=["POST"])
def manage_questions():
    return manage_assessment_questions()

@app.route(BASE_URL + "upload_project_submission_by_user", methods=["POST"])
def upload_project_submission_route():
    return upload_project()
@app.route(BASE_URL + "get_user_weekly_streak", methods=["POST"])
def get_user_weekly_streak_route():
    return get_user_weekly_streak()


@app.route(BASE_URL + "admin/get_course_video_mapping", methods=["GET"])
def admin_get_course_video_mapping_route():
    return get_all_course_video_mapping()

@app.route(BASE_URL + "admin/save_course_video", methods=["POST"])
def admin_save_course_video_route():
    return save_course_video()


def check_db_connection():
    conn = None


if __name__ == "__main__":
    check_db_connection()
    port = int(os.environ.get("PORT", 8000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    print(f"Server running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
