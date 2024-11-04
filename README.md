<p align="center"><img src="https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN@master/img/server/readme/KazeCaptchaAPI/003.webp" alt="KazeCryptoAPI"
    height="300"/></p>


<h1 style="line-height:1;" align="center"><b>KazeCaptchaAPI</b></h1>
<h3>		还在手搓图像验证码识别、计算滑块验证码的偏移距离吗？或是说在你所要使用的编程语言不方便调用OpenCV来进行验证码识别操作？不如试试这个项目，部署一个在线识别验证码接口到你的个人服务器上，无论你所使用什么工具，只需发起一个简单的POST请求，携带你自动获取到的验证码图片，即可在你的服务器上远程处理，并响应给你所需要的识别结果。</h3>
<p align="center"><p align="center"><img src="https://img.shields.io/badge/Python-276DC3?style=for-the-badge&logo=python&logoColor=white" />
</p>

> ## 在线体验（限时开放）：https://vc.uc1.icu

1. ### 滑块距离识别基于：[opencv-python](https://github.com/opencv/opencv-python)

2. ### 图像内容识别基于：[ddddocr](https://github.com/sml2h3/ddddocr)

3. ### 开发框架使用：[Flask](https://github.com/pallets/flask)

> # 部署

> ## 开发环境

### 拉取源码

```
git clone https://github.com/4444TENSEI/KazeCaptchaAPI.git
```

### 安装依赖

```
pip install -r requirements.txt
```

### 启动

```
py main.py
```

##### 默认启动端口号8446，可以在config.ini自行修改，带有几个简单的静态示例页面，服务面板用宝塔比较方便只需简单配置。

```
http://localhost:8446
```

> ## 部署到服务器

将源码压缩包保存到服务器后，用某面板几步就操作部署好了。但由于opencv-python包和ddddocr包的依赖较大，网速不好的安装可能需要十分钟左右，这个速度就看你服务器的带宽和地理位置在哪了。

![](https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN@master/img/server/readme/KazeCaptchaAPI/001.webp)

> # 接口文档

- 本地查看：`/docs/swagger.html`

- 手动导入：将项目目录下的`/docs/swagger.json`导入到你常用的接口测试工具，例如`Apifox`、`Apipost`、`Postman`，格式为`OpenAPI3.0/Swagger`。

> ## 配置文件

项目根目录下的`config.ini`，暂时只有3个配置，分别是`Debug开关`、`文件单次上传大小限制（byte）`、`服务运行端口号`。

```
[app]
DEBUG = True
MAX_CONTENT_LENGTH = 524288
PORT = 8446
```

> ## 其他实现的功能

- IP访问日志：自动记录访问者IP与响应结果产生到`./运行日志.log`文件，默认设置为最大5MB和保留7天。需修改则查看`/common/middleware/log.py`。
- 上传大小限制：使用flask自带的`app.config`配置。
- 细分到每一个路由的请求频繁限制：`/common/middleware/frequency.py`，使用方式是在要做限流的接口路由函数上方，参考修改👇

```
# 导入本地写好的中间件
from common.middleware.frequency import kaze_frequency
# 限制同一IP每分钟最多请求20次此路由
@kaze_frequency("20 per minute")
```

> 
>
> ## 测试

这里有几张图片，保存到设备中，访问[在线体验地址](https://vc.uc1.icu)体验一下纯HTML调用接口实现的验证码识别简单流程，当然更建议自行部署后调自己的接口，毕竟在线体验嘛随时可能趴下。自行部署后在接口测试工具中参照文档发起POST请求试试吧~

![](common/asset/test_img/captcha_img.png)

![](common/asset/test_img/slider_bg.png)

![](common/asset/test_img/slider_piece.png)