import asyncio
import os
import socket
import time
from collections import defaultdict
from typing import Annotated

import redis.asyncio as redis
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Container Appsがレプリカごとに入れてくれる環境変数
REPLICA = os.getenv("CONTAINER_APP_REPLICA_NAME", socket.gethostname())

# プロセス内メモリに状態を持つ（Lab 5でこれが問題になる）
counts: dict[str, int] = defaultdict(int)

# アプリケーションの起動時刻を記録
STARTED_AT = time.monotonic()


@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "uptime": time.monotonic() - STARTED_AT,
    }


@app.get("/api/whoami")
async def whoami():
    return {"replica": REPLICA, "version": 2}


@app.get("/api/work")
async def work():
    await asyncio.sleep(0.5)  # 重い処理のつもり
    return {"replica": REPLICA}


r = redis.from_url(os.environ["REDIS_URL"], decode_responses=True)


@app.post("/api/counter")
async def counter(x_session_id: Annotated[str, Header()]):
    key = f"count:{x_session_id}"
    count = await r.incr(key)  # アトミックなので同時アクセスでもずれない
    await r.expire(key, 3600)  # セッションの有効期限
    return {"count": count, "replica": REPLICA}
