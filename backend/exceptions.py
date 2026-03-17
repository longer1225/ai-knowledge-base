# 原 BusinessException 保留（基础业务异常）
class BusinessException(Exception):
    def __init__(self, msg: str = "操作失败", code: int = 400):
        self.msg = msg
        self.code = code
        super().__init__(self.msg)

# 1. 参数错误异常（前端传参错了）
class ParamException(BusinessException):
    def __init__(self, msg: str = "参数错误"):
        super().__init__(msg=msg, code=400)

# 2. 未登录 / 登录过期
class UnauthorizedException(BusinessException):
    def __init__(self, msg: str = "请先登录"):
        super().__init__(msg=msg, code=401)

# 3. 无权限访问
class ForbiddenException(BusinessException):
    def __init__(self, msg: str = "无权限访问"):
        super().__init__(msg=msg, code=403)

# 4. 数据不存在
class NotFoundException(BusinessException):
    def __init__(self, msg: str = "数据不存在"):
        super().__init__(msg=msg, code=404)