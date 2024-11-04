import logging
from logging.handlers import RotatingFileHandler
from flask import request, jsonify, Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Set up logging
log_file = "运行日志.log"
handler = RotatingFileHandler(
    log_file, maxBytes=5 * 1024 * 1024, backupCount=7, encoding="utf-8"
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger("KAZE")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Create a Blueprint for the normal captcha
normal_captcha = Blueprint("normal_captcha", __name__)

# Initialize ddddocr
import ddddocr

ocr = ddddocr.DdddOcr(show_ad=False)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


def log_request_info(app):
    @app.after_request
    def log_after_request(response):
        if request.path != "/favicon.ico":
            logger.info(
                f"IP: {request.remote_addr} - 请求路由: {request.path} - 请求方法: {request.method} - 响应码: {response.status_code}"
            )
        return response

    @app.errorhandler(Exception)
    def log_exception(error):
        logger.error(f"错误: {error}")
        return jsonify({"code": 500, "message": "Accidental error!"}), 500

    @app.errorhandler(429)
    def ratelimit_error(e):
        logger.warning(f"IP: {request.remote_addr} - Rate limit exceeded.")
        return jsonify({"code": 429, "message": "Rate limit exceeded"}), 429

    @app.errorhandler(413)
    def request_entity_too_large(error):
        allowed_size = app.config["MAX_CONTENT_LENGTH"]
        request_size = request.content_length
        return (
            jsonify(
                {
                    "code": 413,
                    "message": "The request payload is too large!",
                    "allowed_size": allowed_size,
                    "request_size": request_size,
                }
            ),
            413,
        )


def kaze_log(app):
    log_request_info(app)
