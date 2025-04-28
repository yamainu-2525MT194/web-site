# backend/migrations/env.py

import os
import sys
from logging.config import fileConfig

from dotenv import load_dotenv
from alembic import context
from sqlalchemy import engine_from_config, pool

# -----------------------------------------------------------------------------
# 1) .env のパスを明示して読み込む
# -----------------------------------------------------------------------------
# env.py の位置から一階層上の backend ディレクトリに .env がある前提
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)  # ここで確実に .env を読み込む

# -----------------------------------------------------------------------------
# 2) モジュール検索パスに backend を追加 (db.py, models.py を import 可能に)
# -----------------------------------------------------------------------------
sys.path.append(BASE_DIR)

# -----------------------------------------------------------------------------
# 3) Alembic 設定オブジェクトの取得 & logging 設定
# -----------------------------------------------------------------------------
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -----------------------------------------------------------------------------
# 4) .env の DATABASE_URL を文字列として取得し、必ず設定に流し込む
# -----------------------------------------------------------------------------
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL is not set in .env!")
config.set_main_option("sqlalchemy.url", database_url)

# -----------------------------------------------------------------------------
# 5) SQLAlchemy メタデータの指定
# -----------------------------------------------------------------------------
from db import Base
# 必要なら models をインポートしておく
# from models import User, Task
target_metadata = Base.metadata

# 以下、自動生成の run_migrations_offline/run_migrations_online...
