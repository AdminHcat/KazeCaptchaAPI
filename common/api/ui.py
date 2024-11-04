from common.middleware.frequency import kaze_frequency
from flask import Blueprint, render_template

# 静态资源目录
default_pages = Blueprint("default_pages", __name__, template_folder="../asset")


# 首页
@default_pages.route("/")
@kaze_frequency("20 per minute")
def home_page():
    return render_template("index.html")


# 普通图片验证码识别接口示例
@default_pages.route("/normal")
@kaze_frequency("20 per minute")
def normal_page():
    return render_template("test_normal.html")


# 滑块验证码识别接口示例
@default_pages.route("/slider")
@kaze_frequency("20 per minute")
def slider_page():
    return render_template("test_slider.html")


# 404错误页面
@default_pages.app_errorhandler(404)
@kaze_frequency("20 per minute")
def page_not_found(e):
    return render_template("404.html")
