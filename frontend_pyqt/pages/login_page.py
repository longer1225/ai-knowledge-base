from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class LoginPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        # 外层居中布局
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 登录卡片容器
        card = QWidget()
        card.setFixedSize(400, 350)
        card.setStyleSheet("""
            QWidget {
                background-color: #2F2F2F;
                border-radius: 12px;
                border: 1px solid #424242;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("欢迎登录")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; border: none; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.user = QLineEdit()
        self.user.setPlaceholderText("请输入用户名")
        self.user.setFixedHeight(45)

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("请输入密码")
        self.pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd.setFixedHeight(45)

        btn = QPushButton("登 录")
        btn.setFixedHeight(45)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF; color: #000000;
                font-weight: bold; border-radius: 8px; font-size: 16px;
            }
            QPushButton:hover { background-color: #E0E0E0; }
        """)
        btn.clicked.connect(self.login)

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.user)
        layout.addWidget(self.pwd)
        layout.addSpacing(10)
        layout.addWidget(btn)

        main_layout.addWidget(card)

    def login(self):
        u = self.user.text().strip()
        p = self.pwd.text().strip()

        if not u or not p:
            QMessageBox.warning(self, "提示", "请输入账号密码")
            return

        try:
            res = self.main.req.post("/api/user/login", {"username": u, "password": p})
            if res and res.get("code") == 0:
                self.main.state["token"] = res["data"]["access_token"]

                # 新建聊天
                chat_res = self.main.req.post("/api/chat/new", {})
                if chat_res and chat_res.get("code") == 0:
                    self.main.state["chat_id"] = chat_res["data"]["chat_id"]

                # 🚨 通知主窗口登录成功，展示侧边栏并跳转
                self.main.login_success(u)
            else:
                QMessageBox.warning(self, "错误", res.get("msg", "登录失败"))
        except Exception as e:
            QMessageBox.critical(self, "网络错误", f"无法连接服务器：{e}")