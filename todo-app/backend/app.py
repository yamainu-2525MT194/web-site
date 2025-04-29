# backend/app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from passlib.hash import bcrypt
from dotenv import load_dotenv
import os

from db import SessionLocal
from models import User, Task

# ここから自動テーブル作成用インポート
from db import engine, Base
# モデルをインポートしてから create_all を呼び出す
Base.metadata.create_all(bind=engine)

# 環境変数読み込み
load_dotenv()

app = Flask(__name__)
CORS(app)

# JWT 設定
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# ───── 認証用エンドポイント ─────

@app.post("/auth/register")
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400

    db = SessionLocal()
    if db.query(User).filter_by(username=username).first():
        return jsonify({"msg": "username already exists"}), 409

    hashed_pw = bcrypt.hash(password)
    user = User(username=username, password_hash=hashed_pw)
    db.add(user); db.commit()
    return jsonify({"msg": "user created"}), 201

@app.post("/auth/login")
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400

    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()

    if not user or not bcrypt.verify(password, user.password_hash):
        return jsonify({"msg": "Bad credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200

# ───── タスク用エンドポイント（JWT 保護付き） ─────

@app.get("/api/tasks")
@jwt_required()
def get_tasks():
    # 文字列 → 整数に戻す
    current_user_id = int(get_jwt_identity())
    db = SessionLocal()
    task_objs = db.query(Task).filter_by(owner_id=current_user_id).all()
    result = [{"id": t.id, "title": t.title, "done": t.done} for t in task_objs]
    return jsonify(result), 200

@app.post("/api/tasks")
@jwt_required()
def add_task():
    current_user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"msg": "title is required"}), 400

    db = SessionLocal()
    new_task = Task(title=title, done=False, owner_id=current_user_id)
    db.add(new_task); db.commit(); db.refresh(new_task)
    return jsonify({"id": new_task.id, "title": new_task.title, "done": new_task.done}), 201

# ───── アプリ起動 ─────

if __name__ == "__main__":
    # コンテナ外からアクセス可能に 0.0.0.0 を指定
    app.run(host="0.0.0.0", port=5000)
