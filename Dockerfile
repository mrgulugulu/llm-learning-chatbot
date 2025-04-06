# 使用官方的 Python 作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /workspace

# 复制 requirements.txt 文件（如果有）
COPY requirements.txt ./

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/


# 复制源代码
COPY . .

# 暴露应用运行的端口
EXPOSE 5010

# 启动应用
CMD ["python", "app.py"]