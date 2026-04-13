# from logger_config import logger
# from functools import wraps
# from flask import request
# import time


# def get_user_id():
#     """Extract user_id from all possible sources"""
#     try:
#         return (
#             request.args.get("user_id") or
#             request.args.get("userId") or
#             (request.json.get("user_id") if request.is_json and request.json else None) or
#             (request.json.get("userId") if request.is_json and request.json else None) or
#             request.form.get("user_id") or
#             "anonymous"
#         )
#     except Exception:
#         return "anonymous"


# def log_api(api_name):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):

#             user_id = get_user_id()

#             log_context = {
#                 "api": api_name,
#                 "function": func.__name__,
#                 "user_id": user_id
#             }

#             start_time = time.time()

#             # ✅ START LOG
#             logger.info(
#                 f"START {api_name} | user_id={user_id} | function={func.__name__}",
#                 extra={"custom_dimensions": log_context}
#             )

#             try:
#                 response = func(*args, **kwargs)

#                 duration = round((time.time() - start_time) * 1000, 2)

#                 # ✅ SUCCESS LOG
#                 logger.info(
#                     f"SUCCESS {api_name} | user_id={user_id} | time={duration}ms",
#                     extra={
#                         "custom_dimensions": {
#                             **log_context,
#                             "response_time_ms": duration
#                         }
#                     }
#                 )

#                 return response

#             except Exception as e:
#                 duration = round((time.time() - start_time) * 1000, 2)

#                 # ❗ ERROR LOG
#                 logger.exception(
#                     f"ERROR {api_name} | user_id={user_id} | time={duration}ms",
#                     extra={
#                         "custom_dimensions": {
#                             **log_context,
#                             "response_time_ms": duration
#                         }
#                     }
#                 )
#                 raise

#         return wrapper
#     return decorator




from logger_config import logger
from functools import wraps
from flask import request
import time


# def log_api(api_name):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):

#             log_context = {
#                 "api": api_name,
#                 "function": func.__name__
#             }

#             start_time = time.time()

#             # START LOG
#             logger.info(
#                 f"START | API={api_name}",
#                 extra={"custom_dimensions": {**log_context, "status": "START"}}
#             )

#             try:
#                 response = func(*args, **kwargs)

#                 duration = round((time.time() - start_time) * 1000, 2)

#                 # SUCCESS LOG
#                 logger.info(
#                     f"SUCCESS | API={api_name} | {duration}ms",
#                     extra={
#                         "custom_dimensions": {
#                             **log_context,
#                             "status": "SUCCESS",
#                             "response_time_ms": duration
#                         }
#                     }
#                 )

#                 return response

#             except Exception as e:

#                 duration = round((time.time() - start_time) * 1000, 2)

#                 # ERROR LOG (stack trace included)
#                 logger.exception(
#                     f"ERROR | API={api_name} | {duration}ms | {str(e)}",
#                     extra={
#                         "custom_dimensions": {
#                             **log_context,
#                             "status": "ERROR",
#                             "response_time_ms": duration,
#                             "error": str(e)
#                         }
#                     }
#                 )
#                 raise

#         return wrapper
#     return decorator




def log_api(api_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            log_context = {
                "api": api_name,
                "function": func.__name__,
                "method": request.method,
                "path": request.path
            }

            start_time = time.time()

            # START LOG
            logger.info(
                f"START | API={api_name}",
                extra={"custom_dimensions": {**log_context, "status": "START"}}
            )

            try:
                response = func(*args, **kwargs)

                duration = round((time.time() - start_time) * 1000, 2)

                # 🔥 IMPORTANT: response status check
                status_code = response[1] if isinstance(response, tuple) else 200

                if status_code >= 500:
                    logger.error(
                        f"ERROR RESPONSE | API={api_name} | {status_code} | {duration}ms",
                        extra={
                            "custom_dimensions": {
                                **log_context,
                                "status": "ERROR",
                                "status_code": status_code,
                                "response_time_ms": duration
                            }
                        }
                    )
                elif status_code >= 400:
                    logger.warning(
                        f"CLIENT ERROR | API={api_name} | {status_code} | {duration}ms",
                        extra={
                            "custom_dimensions": {
                                **log_context,
                                "status": "FAIL",
                                "status_code": status_code,
                                "response_time_ms": duration
                            }
                        }
                    )
                else:
                    logger.info(
                        f"SUCCESS | API={api_name} | {duration}ms",
                        extra={
                            "custom_dimensions": {
                                **log_context,
                                "status": "SUCCESS",
                                "response_time_ms": duration
                            }
                        }
                    )

                return response

            except Exception as e:

                duration = round((time.time() - start_time) * 1000, 2)

                logger.exception(
                    f"EXCEPTION | API={api_name} | {duration}ms",
                    extra={
                        "custom_dimensions": {
                            **log_context,
                            "status": "ERROR",
                            "response_time_ms": duration,
                            "error": str(e)
                        }
                    }
                )
                raise

        return wrapper
    return decorator