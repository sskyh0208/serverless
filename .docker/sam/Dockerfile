FROM --platform=linux/amd64 python:3.12

RUN apt-get update
RUN apt-get install -y jq wget gettext zip less vim git docker.io make


RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

RUN curl -OL "https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip"
RUN unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
RUN ./sam-installation/install

COPY ./requirements.txt /home/sam/requirements.txt
RUN pip install -U pip && \
    pip install -r /home/sam/requirements.txt

WORKDIR /home/sam/src