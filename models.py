from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建唯一的SQLAlchemy实例
db = SQLAlchemy()

class NormData(db.Model):
    """常模数据模型"""
    __tablename__ = "norm_data"
    id = db.Column(db.Integer, primary_key=True)
    dimension = db.Column(db.String(50), unique=True, nullable=False)
    p25 = db.Column(db.Float, nullable=False)
    p50 = db.Column(db.Float, nullable=False)
    p75 = db.Column(db.Float, nullable=False)
    low_threshold = db.Column(db.Float, nullable=False)
    high_threshold = db.Column(db.Float, nullable=False)

class UserResult(db.Model):
    """用户测评结果模型"""
    __tablename__ = "user_results"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.Integer)
    q9 = db.Column(db.Integer)
    q10 = db.Column(db.Integer)
    q11 = db.Column(db.Integer)
    q12 = db.Column(db.Integer)
    q13 = db.Column(db.Integer)
    q14 = db.Column(db.Integer)
    q15 = db.Column(db.Integer)
    dimension1 = db.Column(db.Float)  # 评价恐惧维度（1-5题）
    dimension2 = db.Column(db.Float)  # 隐私担忧维度（6-9题）
    dimension3 = db.Column(db.Float)  # 交往焦虑维度（10-15题）
    total_score = db.Column(db.Float)  # 总分
    total_level = db.Column(db.String(50))
    dim1_level = db.Column(db.String(50))
    dim2_level = db.Column(db.String(50))
    dim3_level = db.Column(db.String(50))
    total_percentile = db.Column(db.String(100))
    dim1_percentile = db.Column(db.String(100))
    dim2_percentile = db.Column(db.String(100))
    dim3_percentile = db.Column(db.String(100))