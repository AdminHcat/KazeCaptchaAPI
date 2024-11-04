from common.middleware.frequency import kaze_frequency
from flask import Blueprint, jsonify, request
from io import BytesIO
import ddddocr

normal_captcha = Blueprint("normal_captcha", __name__)
# 初始化ddddocr
ocr = ddddocr.DdddOcr(show_ad=False)


# 接收普通图片验证码图片文件的接口, 最终响应json, 识别结果为captcha的值
@normal_captcha.route("/normal", methods=["POST"])
# 访问频率限制中间件, 这里限制同一IP每分钟最多请求10次此路由
@kaze_frequency("10 per minute")
def normal_route():
    captcha_img = request.files.get("captcha_img")
    if not captcha_img:
        return jsonify(
            {
                "code": 400,
                "message": "Must upload 'captcha_img' files!",
            }
        )
    captcha_img = BytesIO(captcha_img.read())
    return jsonify({"captcha": ocr.classification(captcha_img.getvalue())})
