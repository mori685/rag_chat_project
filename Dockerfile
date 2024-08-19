# Python 3.9をベースイメージとして使用
FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# エントリーポイントスクリプトに実行権限を付与
RUN chmod +x /app/entrypoint.sh

# エントリーポイントを設定
ENTRYPOINT ["/app/entrypoint.sh"]