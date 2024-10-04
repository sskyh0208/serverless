FROM --platform=linux/amd64 python:3.12

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y jq wget gettext zip less vim git curl unzip docker.io

# Node.js のインストール
ENV NVM_DIR /root/.nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && \
    export NVM_DIR="/root/.nvm" && \
    . $NVM_DIR/nvm.sh && \
    nvm install 22.8.0 && \
    nvm use 22.8.0 && \
    npm install -g aws-cdk

# AWS CLI v2 のインストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

# Python パッケージのインストール
COPY ./requirements.txt /home/cdk/requirements.txt
RUN pip install -U pip && \
    pip install -r /home/cdk/requirements.txt

# PATH の設定
ENV PATH="/root/.nvm/versions/node/v22.8.0/bin:${PATH}"

# 作業ディレクトリの設定
WORKDIR /home/cdk/src