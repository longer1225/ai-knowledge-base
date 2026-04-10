from sqlalchemy import inspect
from typing import Any, Dict, List
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


def to_dict(obj: Any) -> Dict | List[Dict] | None:
    """
    通用 SQLAlchemy ORM → 字典转换工具
    ✅ 支持单对象 / 列表
    ✅ 支持 datetime / date / Decimal / Enum
    ✅ 结果可直接 JSON 序列化（可存 Redis）
    """

    if obj is None:
        return None

    # ✅ 列表处理（递归）
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]

    # ✅ 非 ORM 对象直接返回（兜底）
    try:
        mapper = inspect(obj).mapper
    except Exception:
        return obj

    result = {}

    for col in mapper.columns:
        value = getattr(obj, col.name)

        # ======================
        # 🔥 类型安全转换（关键）
        # ======================

        # datetime → str
        if isinstance(value, datetime):
            value = value.isoformat()

        # date → str
        elif isinstance(value, date):
            value = value.isoformat()

        # Decimal → float（或 str 看你需求）
        elif isinstance(value, Decimal):
            value = float(value)

        # Enum → value
        elif isinstance(value, Enum):
            value = value.value

        result[col.name] = value

    return result