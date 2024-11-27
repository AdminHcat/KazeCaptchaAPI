# 使用官方的 Python 3.9 运行时作为父镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 当前目录内容复制到容器的 /app 中
COPY . /app

# 安装依赖项  --no-cache-dir（不适用缓存的依赖，将重下依赖，耗时久但镜像体积较小）
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8446

# 运行应用
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8446"]
