# 从仓库拉取 带有 python 3.6 的 Linux 环境
FROM python:3.6

# 设置环境变量
ENV PYTHONUNBUFFERED 1

# 安装连接数据库的库
RUN echo -e 'https://mirrors.aliyun.com/alpine/v3.6/main/\nhttps://mirrors.aliyun.com/alpine/v3.6/community/' > /etc/apt/repositories
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev -y

#RUN apk add python3-dev default-libmysqlclient-dev -y

# 在根目录新建一个code文件夹，工程代码放在这里面
RUN mkdir /code

# 工作目录切换到code目录下
WORKDIR /code

# 升级pip
RUN pip install pip -U
# 依赖的文件从宿主机加载到docker容器中
ADD requirements.txt /code/

# 从清华的镜像安装依赖的python包
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

# 把本目录所有的文件拷到容器中
ADD . /code/
