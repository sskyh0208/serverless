# ベースイメージ
FROM python:3.12 AS base

# ソースコードのコピーと作業ディレクトリの設定
COPY ./ /api
WORKDIR /api

# ロケール設定
RUN apt-get update && \
    apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    apt-get install -y vim less wget gettext zip less jq && \
    rm -rf /var/lib/apt/lists/*

# 環境変数の設定
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# pipとpoetryのインストール
RUN pip install --upgrade pip && \
    pip install poetry

# Poetryの仮想環境を無効化
RUN poetry config virtualenvs.create false

# ポート設定
ENV PORT=8000
EXPOSE 8000

##################################################
# 開発環境用イメージ
##################################################
FROM base AS dev

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

##################################################
# ステージング環境用イメージ
##################################################
FROM base AS stg

# AWS Lambda Adapterの追加
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

# Poetryで依存関係をインストール
RUN poetry install --only main --no-interaction --no-ansi

# アプリケーションの起動コマンド
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT


##################################################
# 本番環境用イメージ
##################################################
FROM base AS prod

# AWS Lambda Adapterの追加
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

# Poetryで依存関係をインストール
RUN poetry install --only main --no-interaction --no-ansi

# アプリケーションの起動コマンド
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
