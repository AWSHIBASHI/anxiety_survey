from flask import Flask
import os
from models import db  # 只导入db实例，不导入模型


def create_app():
    app = Flask(__name__)

    # 数据库配置
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "db", "anxiety.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path.replace(os.sep, '/')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 初始化SQLAlchemy
    db.init_app(app)

    # 注册模板过滤器
    @app.template_filter('level_class')
    def get_level_class(level):
        """根据焦虑等级返回对应的CSS类名"""
        if level == "低水平焦虑":
            return "level-low"
        elif level == "中等水平焦虑":
            return "level-medium"
        elif level == "高水平焦虑":
            return "level-high"
        else:
            return "level-unknown"

    with app.app_context():
        # 确保数据库文件夹存在
        os.makedirs(os.path.join(app.root_path, "db"), exist_ok=True)

        # 导入模型（仅在需要时导入）
        from models import NormData, UserResult

        # 创建表结构
        db.create_all()

        # 插入常模数据（确保只插入一次）
        if not NormData.query.first():
            insert_norm_data()

    # 注册蓝图（避免循环导入，放在最后）
    import routes
    app.register_blueprint(routes.bp)

    return app


def insert_norm_data():
    """插入常模数据"""
    from models import NormData
    norms = [
        {
            "dimension": "总分",
            "p25": 56,
            "p50": 63,
            "p75": 67,
            "low_threshold": 39,
            "high_threshold": 72
        },
        {
            "dimension": "评价恐惧",
            "p25": 17.25,
            "p50": 22,
            "p75": 22,
            "low_threshold": 13,
            "high_threshold": 24
        },
        {
            "dimension": "隐私担忧",
            "p25": 14,
            "p50": 17,
            "p75": 18,
            "low_threshold": 10,
            "high_threshold": 19
        },
        {
            "dimension": "交往焦虑",
            "p25": 22,
            "p50": 25,
            "p75": 27,
            "low_threshold": 15,
            "high_threshold": 29
        }
    ]
    for norm in norms:
        db.session.add(NormData(**norm))
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)