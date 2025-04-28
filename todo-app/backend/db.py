import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env を読み込む
load_dotenv()

# DATABASE_URL は .env に設定済み
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy エンジン作成
engine = create_engine(
    DATABASE_URL,
    echo=True,        # SQL ログを出す（開発時は便利）
    future=True,      # 2.0 スタイルの API
)

# セッションファクトリ
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

# ベースクラス
Base = declarative_base()
