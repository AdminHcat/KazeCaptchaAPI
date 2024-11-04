from common.middleware.frequency import kaze_frequency
from flask import request, jsonify, Blueprint
import numpy as np
import cv2

slider_captcha = Blueprint("slider_captcha", __name__)


# 接收验证码拼图和背景图片文件的接口, 最终响应json包含的offset的值即为需要水平移动的像素值
@slider_captcha.route("/slider", methods=["POST"])
# 访问频率限制中间件, 这里限制同一IP每分钟最多请求10次此路由
@kaze_frequency("10 per minute")
def slider_route():
    slider_img = request.files.get("slider_piece")
    slider_bg = request.files.get("slider_bg")
    if not slider_img or not slider_bg:
        return jsonify(
            {
                "code": 400,
                "message": "Must upload 'slider_piece' and 'slider_bg' files!",
            }
        )
    piece_img = cv2.imdecode(
        np.frombuffer(slider_img.read(), np.uint8), cv2.IMREAD_GRAYSCALE
    )
    bg_img = cv2.imdecode(
        np.frombuffer(slider_bg.read(), np.uint8), cv2.IMREAD_GRAYSCALE
    )
    offset = calculate_offset(piece_img, bg_img)
    return jsonify({"offset": offset})


# 滑块距离计算核心: 计算滑块图片与背景图片之间的偏差距离, 顺便处理了拼图宽高可能大于背景的情况
def calculate_offset(piece_img, bg_img):
    piece_height, piece_width = piece_img.shape[:2]
    bg_height, bg_width = bg_img.shape[:2]
    if piece_width > bg_width or piece_height > bg_height:
        scale_width = bg_width / piece_width
        scale_height = bg_height / piece_height
        scale_factor = min(scale_width, scale_height)
        piece_img = cv2.resize(
            piece_img,
            None,
            fx=scale_factor,
            fy=scale_factor,
            interpolation=cv2.INTER_AREA,
        )
    piece_img = cv2.Canny(piece_img, 255, 255)
    bg_img = cv2.Canny(bg_img, 255, 255)
    result = cv2.matchTemplate(bg_img, piece_img, cv2.TM_CCOEFF_NORMED)
    # 这里只用到一个但是其他的也先留着吧
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc[0]
