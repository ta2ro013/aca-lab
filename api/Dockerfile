FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.29 /uv /uvx /bin/

# アプリ専用の一般ユーザーを作る（UIDは数字で指定できるよう固定）
RUN groupadd --system --gid 10001 app \
 && useradd --system --uid 10001 --gid app --no-create-home app

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
# イメージに入っているPythonを使う。
ENV UV_PYTHON_DOWNLOADS=never

# 依存だけ先に入れる
#main.py を変えても、このレイヤーはキャッシュが効く）
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project --no-cache

COPY api/main.py .
ENV PATH="/app/.venv/bin:$PATH"

# 実行時は一般ユーザーで動かす。
# ファイルの持ち主は root のままなので、アプリからはコードも依存も書き換えられない
USER 10001:10001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
