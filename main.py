from flask import Flask
from flask_cors import CORS
from common.config.load import load_config
from common.middleware.log import kaze_log
from common.middleware.frequency import limiter
from common.api.ui import default_pages, page_not_found
from common.api.slider import slider_captcha
from common.api.normal import normal_captcha


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # 设置请求频率限制器
    limiter.init_app(app)
    # 访问日志中间件
    kaze_log(app)
    # 捕捉404页面
    app.register_error_handler(404, page_not_found)
    # 主要API服务
    app.register_blueprint(slider_captcha)
    app.register_blueprint(normal_captcha)
    app.register_blueprint(default_pages)

    return app


if __name__ == "__main__":
    debug, port, max_content_length = load_config()
    app = create_app()
    app.config.update(MAX_CONTENT_LENGTH=max_content_length)
    app.run(debug=debug, port=port)
