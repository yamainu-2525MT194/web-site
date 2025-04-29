
from flask import Flask, jsonify, request
from flask_cors import CORS


# ★ 追加分：JWT とパスワードハッシュ用
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from passlib.hash import bcrypt

# 環境変数読み込み
from dotenv import load_dotenv
load_dotenv()
import os

# DB セッションとモデル
from db import SessionLocal
from models import User, Task

app = Flask(__name__)
CORS(app)

# ★ 追加分：JWT シークレットキーを設定
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

tasks = [
    {"id": 1, "title": "Learn Python", "done": False},
    {"id": 2, "title": "Learn React", "done": False},
]

@app.get("/api/tasks")
@jwt_required()
def get_tasks():
    # 1) トークンからユーザーIDを取得
    current_user_id = get_jwt_identity()
    
    # 2) DB セッション生成
    db = SessionLocal()
    
    # 3) 当該ユーザーのタスクだけを取得
    task_objs = db.query(Task).filter_by(owner_id=current_user_id).all()
    
    # 4) JSON シリアライズ用リストに変換
    result = [
      {"id": t.id, "title": t.title, "done": t.done}
      for t in task_objs
    ]
    return jsonify(result), 200

@app.post("/api/tasks")
@jwt_required()
def add_task():
    # 1) トークンからユーザーIDを取得
    current_user_id = get_jwt_identity()
    
    # 2) リクエスト JSON 取得
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"msg": "title is required"}), 400

    # 3) DB セッション
    db = SessionLocal()

    # 4) Task インスタンス生成・保存
    new_task = Task(
      title=title,
      done=False,
      owner_id=current_user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)  # ID など最新情報を取得

    # 5) レスポンス
    return jsonify({
      "id": new_task.id,
      "title": new_task.title,
      "done": new_task.done
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


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

    # 入力チェック
    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400

    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()

    # ユーザー存在＆パスワード検証
    if not user or not bcrypt.verify(password, user.password_hash):
        return jsonify({"msg": "Bad credentials"}), 401

    # JWT 発行（identity にユーザーIDをセット）
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200
