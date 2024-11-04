from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask import Blueprint

normal_captcha = Blueprint("normal_captcha", __name__)
limiter = Limiter(key_func=get_remote_address)


# 访问频率限制中间件
def kaze_frequency(limit_count, methods=None):
    def decorator(route):
        return limiter.limit(
            limit_count, methods=methods, error_message="Rate limit exceeded"
        )(route)

    return decorator
