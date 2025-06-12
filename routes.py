from flask import Blueprint, render_template, request, jsonify, make_response, current_app
from datetime import datetime
from models import db, NormData, UserResult  # 从models.py导入模型

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    """首页路由：显示测评介绍"""
    return render_template('index.html')

@bp.route('/questionnaire')
def questionnaire():
    """问卷页面路由"""
    return render_template('questionnaire.html')


@bp.route('/api/questionnaire', methods=['GET'])
def get_questionnaire():
    """获取问卷题目API"""
    questions = [
        {"id": 1, "text": "通过微信与导师沟通工作时，我会逐字检查每条信息内容", "dimension": "评价恐惧"},
        {"id": 2, "text": "看到同学在社交媒体展示科研成果时，我会感到焦虑", "dimension": "评价恐惧"},
        {"id": 3, "text": "当看到同学在学术群组展示科研成果时，我会因比较压力放弃发言", "dimension": "评价恐惧"},
        {"id": 4, "text": "当在朋友圈发布生活动态后，我会担心被导师/同学看到后质疑，最终设置'仅自己可见'",
         "dimension": "评价恐惧"},
        {"id": 5, "text": "我会删除朋友圈中可能引发争议的动态", "dimension": "评价恐惧"},
        {"id": 6, "text": "我经常调整朋友圈分组来限制不同人群的信息可见范围", "dimension": "隐私担忧"},
        {"id": 7, "text": "在陌生平台（如小红书）发布内容时，我会隐藏个人真实信息", "dimension": "隐私担忧"},
        {"id": 8, "text": "当APP要求获取通讯录权限时，我会感到不安", "dimension": "隐私担忧"},
        {"id": 9, "text": "线上小组讨论时，我会因发言内容被记录产生顾虑", "dimension": "隐私担忧"},
        {"id": 10, "text": "当社交媒体（如微信、QQ、小红书等）上与新添加的人交流会让我感到焦虑", "dimension": "交往焦虑"},
        {"id": 11,
         "text": "当线上会议（如腾讯会议/Zoom）开启自动字幕或会议记录功能时，我会担心说错话被永久记录下来，从而更不敢发言",
         "dimension": "交往焦虑"},
        {"id": 12, "text": "当朋友超过2小时未回复消息时，我会怀疑自己说错话", "dimension": "交往焦虑"},
        {"id": 13, "text": "当在BOSS直聘等平台向HR发送消息后，若看到'已读未回'状态超过24小时，我会修改个人主页的求职意向",
         "dimension": "交往焦虑"},
        {"id": 14, "text": "在线上会议/答辩时，使用视频（露脸）会让我感到更焦虑", "dimension": "交往焦虑"},
        {"id": 15, "text": "当微信群/QQ群里有人提出'互帮互助'（比如互引论文、互填问卷）的请求时，我会感到被迫参与的压力",
         "dimension": "交往焦虑"}
    ]
    return jsonify(questions)


@bp.route('/api/submit', methods=['POST'])
def submit_assessment():
    """提交测评结果API"""
    with current_app.app_context():
        data = request.json

        # 提取15道题的答案
        responses = [int(data.get(f'q{i}', 3)) for i in range(1, 16)]

        # 计算各维度得分
        dimension1 = sum(responses[0:5])  # 评价恐惧维度
        dimension2 = sum(responses[5:9])  # 隐私担忧维度
        dimension3 = sum(responses[9:15])  # 交往焦虑维度
        total_score = dimension1 + dimension2 + dimension3

        # 获取常模数据
        norm_total = NormData.query.filter_by(dimension='总分').first()
        norm_dim1 = NormData.query.filter_by(dimension='评价恐惧').first()
        norm_dim2 = NormData.query.filter_by(dimension='隐私担忧').first()
        norm_dim3 = NormData.query.filter_by(dimension='交往焦虑').first()

        # 计算百分位
        def get_percentile(score, norm):
            if score < norm.p25:
                return "低于25%的研究生"
            elif score < norm.p50:
                return "处于25%-50%的研究生之间"
            elif score < norm.p75:
                return "处于50%-75%的研究生之间"
            else:
                return "高于75%的研究生"

        # 确定焦虑等级
        def get_level(score, norm):
            if score < norm.low_threshold:
                return "低水平焦虑"
            elif score <= norm.high_threshold:
                return "中等水平焦虑"
            else:
                return "高水平焦虑"

        # 封装结果
        result = {
            "total_score": total_score,
            "dimension1": dimension1,
            "dimension2": dimension2,
            "dimension3": dimension3,
            "total_percentile": get_percentile(total_score, norm_total),
            "total_level": get_level(total_score, norm_total),
            "dim1_percentile": get_percentile(dimension1, norm_dim1),
            "dim1_level": get_level(dimension1, norm_dim1),
            "dim2_percentile": get_percentile(dimension2, norm_dim2),
            "dim2_level": get_level(dimension2, norm_dim2),
            "dim3_percentile": get_percentile(dimension3, norm_dim3),
            "dim3_level": get_level(dimension3, norm_dim3),
            "user_name": data.get('user_name', ''),
            "gender": data.get('gender', ''),
            "age": data.get('age', '')
        }

        # 保存结果到数据库
        if data.get('user_name'):
            user_result = UserResult(
                user_name=data.get('user_name', None),
                gender=data.get('gender'),
                age=data.get('age'),
                q1=responses[0], q2=responses[1], q3=responses[2], q4=responses[3], q5=responses[4],
                q6=responses[5], q7=responses[6], q8=responses[7], q9=responses[8],
                q10=responses[9], q11=responses[10], q12=responses[11],
                q13=responses[12], q14=responses[13], q15=responses[14],
                dimension1=dimension1, dimension2=dimension2, dimension3=dimension3,
                total_score=total_score,
                total_percentile=result["total_percentile"],
                total_level=result["total_level"],
                dim1_percentile=result["dim1_percentile"],
                dim1_level=result["dim1_level"],
                dim2_percentile=result["dim2_percentile"],
                dim2_level=result["dim2_level"],
                dim3_percentile=result["dim3_percentile"],
                dim3_level=result["dim3_level"]
            )
            db.session.add(user_result)
            db.session.commit()

            return jsonify({
                "success": True,
                "result_id": user_result.id
            })
        else:
            # 匿名用户处理
            return jsonify({"error": "结果无法保存，请提供用户名"}), 400


@bp.route('/result')
def result():
    """结果页面路由"""
    return render_template('result.html', result=request.args)

@bp.route('/result/<int:result_id>')
def result_detail(result_id):
    result = UserResult.query.get_or_404(result_id)
    return render_template('result.html',
        result=result,
        now=datetime.now(),
        norm_total=NormData.query.filter_by(dimension='总分').first(),
        norm_dim1=NormData.query.filter_by(dimension='评价恐惧').first(),
        norm_dim2=NormData.query.filter_by(dimension='隐私担忧').first(),
        norm_dim3=NormData.query.filter_by(dimension='交往焦虑').first()
    )


@bp.route('/results/history', methods=['GET'])
def result_history():
    """历史结果查询路由"""
    user_name = request.args.get('user_name')
    if not user_name:
        return jsonify({"error": "请提供用户名"}), 400

    # 查询数据库中的历史结果
    results = UserResult.query.filter_by(user_name=user_name).all()
    history = []
    for result in results:
        history.append({
            "id": result.id,
            "create_time": result.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_score": result.total_score,
            "total_level": result.total_level
        })

    return render_template('result_history.html', history=history, user_name=user_name)