# backend/mapper/history_mapper.py
# 纯数据库CRUD，无任何业务逻辑，用db_connection装饰器自动管理连接
from ..models import QAHistory
from utils.db_util import db_connection  # 导入你的AOP装饰器

# 获取用户QA历史
@db_connection  # 自动注入db参数，自动关闭连接
def get_history_by_user_id(user_id: int, db=None):
    # 只做数据库查询，返回原始数据
    history = db.query(QAHistory).filter(QAHistory.user_id == user_id)\
               .order_by(QAHistory.create_time.desc()).all()
    # 转字典（给Service层用）
    return [
        {
            "qa_id": h.qa_id,
            "question": h.question,
            "answer": h.answer,
            "create_time": h.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        for h in history
    ]

# 插入QA历史
@db_connection
def insert_history(user_id: int, question: str, answer: str, source_chunks="", similarity_scores="", db=None):
    # 只做数据库插入，无业务逻辑
    new_history = QAHistory(
        user_id=user_id,
        question=question,
        answer=answer,
        source_chunks=source_chunks,
        similarity_scores=similarity_scores
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history.qa_id  # 只返回必要的ID，不返回完整对象

# 清空用户QA历史
# 建议补充返回值（方便Service层判断是否执行成功）
@db_connection
def delete_history_by_user_id(user_id: int, db=None):
    # 先查询是否有该用户的记录（可选，增强鲁棒性）
    count = db.query(QAHistory).filter(QAHistory.user_id == user_id).count()
    if count == 0:
        return 0  # 无记录可删
    # 执行删除
    db.query(QAHistory).filter(QAHistory.user_id == user_id).delete()
    db.commit()
    return count  # 返回删除的记录数