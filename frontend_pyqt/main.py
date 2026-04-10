import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


from request_util import RequestUtil
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from pages.upload_page import UploadPage
from pages.manage_page import ManagePage


# ================= 核心修复：侧边栏自定义对话项组件 =================
class ChatListItemWidget(QWidget):
    def __init__(self, chat_id, title, rename_cb, delete_cb):
        super().__init__()
        self.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 0, 2)
        layout.setSpacing(5)

        # 对话标题（设置穿透鼠标点击，这样点击文字也能选中这行列表）
        self.title_lbl = QLabel(f"📝 {title}")
        self.title_lbl.setStyleSheet("color: #CCC; font-size: 14px;")
        self.title_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # 重命名按钮
        btn_rename = QPushButton("✏️")
        btn_rename.setFixedSize(28, 28)
        btn_rename.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_rename.setStyleSheet(
            "QPushButton { background: transparent; border: none; } QPushButton:hover { background: #444; border-radius: 4px; }")
        btn_rename.clicked.connect(lambda: rename_cb(chat_id, title))

        # 删除按钮
        btn_delete = QPushButton("🗑️")
        btn_delete.setFixedSize(28, 28)
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.setStyleSheet(
            "QPushButton { background: transparent; border: none; color: #FF5555; } QPushButton:hover { background: #FF5555; color: white; border-radius: 4px; }")
        btn_delete.clicked.connect(lambda: delete_cb(chat_id))

        layout.addWidget(self.title_lbl)
        layout.addStretch()
        layout.addWidget(btn_rename)
        layout.addWidget(btn_delete)


# ================= 主窗口 =================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 知识库系统")
        self.resize(1200, 800)
        self.center_window()

        self.state = {"token": None, "username": None, "chat_id": None}
        self.req = RequestUtil(self.state)

        # 🚨 全局样式表 🚨
        self.setStyleSheet("""
            QMainWindow, QStackedWidget { background-color: #212121; }
            QWidget { color: #ECECEC; font-size: 14px; font-family: "Microsoft YaHei", "Segoe UI"; }

            #sidebar { background-color: #171717; border-right: 1px solid #2F2F2F; }
            #nav_btn {
                background-color: transparent; border: none; text-align: left;
                padding: 12px 20px; border-radius: 8px; font-size: 15px;
            }
            #nav_btn:hover { background-color: #2F2F2F; }
            #nav_btn:checked { background-color: #383838; font-weight: bold; }

            QLineEdit { background-color: #2F2F2F; border: 1px solid #424242; border-radius: 8px; padding: 10px; color: white; }
            QLineEdit:focus { border: 1px solid #5A5A5A; }

            QScrollBar:vertical { border: none; background: transparent; width: 8px; margin: 0px; }
            QScrollBar::handle:vertical { background: #555; min-height: 30px; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #777; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; }

            QListWidget#history_list { background: transparent; border: none; outline: none; }
            QListWidget#history_list::item { border-radius: 6px; }
            QListWidget#history_list::item:hover { background-color: #2F2F2F; }
            QListWidget#history_list::item:selected { background-color: #383838; }

            /* 👇 终极绝杀：发送按钮的专属样式写在这里！必定生效！ 👇 */
            /* 👇 替换掉你原来的 sendBtn 样式 👇 */
            QPushButton#sendBtn { 
                background-color: #FFFFFF !important; /* 加 !important 强制覆盖 */
                color: #000000 !important;
                border-radius: 25px !important;
                font-weight: bold !important;
                font-size: 15px !important;
                border: 1px solid #FFFFFF !important;
                padding: 5px 15px; /* 加一点内边距，防止文字贴边 */
            }
            QPushButton#sendBtn:hover { 
                background-color: #D0D0D0 !important;
                color: #000000 !important;
                border: 1px solid #D0D0D0 !important;
            }
            QPushButton#sendBtn:disabled { 
                background-color: #444444 !important;
                color: #888888 !important;
                border: 1px solid #444444 !important;
            }
        """)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setCentralWidget(main_widget)

        # ===== 左侧导航栏 =====
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setObjectName("sidebar")
        self.sidebar_widget.setFixedWidth(260)  # 稍微加宽一点，容纳编辑按钮

        sidebar = QVBoxLayout(self.sidebar_widget)
        sidebar.setContentsMargins(15, 30, 15, 20)
        sidebar.setSpacing(10)

        self.user_label = QLabel("未登录")
        self.user_label.setStyleSheet("color: #AAA; font-size:16px; font-weight:bold; margin-bottom: 20px;")
        sidebar.addWidget(self.user_label)

        self.btn_group = QButtonGroup(self)
        self.btn_chat = QPushButton("💬 新聊天")
        self.btn_upload = QPushButton("📤 文档上传")
        self.btn_manage = QPushButton("📖 知识库管理")

        for i, btn in enumerate([self.btn_chat, self.btn_upload, self.btn_manage]):
            btn.setObjectName("nav_btn")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_group.addButton(btn, i)
            sidebar.addWidget(btn)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #333;")
        sidebar.addWidget(line)
        sidebar.addWidget(QLabel("📂 历史对话", styleSheet="color:#888; font-size:12px; margin-top:10px;"))

        self.history_list = QListWidget()
        self.history_list.setObjectName("history_list")
        self.history_list.itemClicked.connect(self.switch_history_chat)
        sidebar.addWidget(self.history_list)

        # ===== 页面区域 =====
        self.stack = QStackedWidget()
        self.login_page = LoginPage(self)
        self.chat_page = ChatPage(self)
        self.upload_page = UploadPage(self)
        self.manage_page = ManagePage(self)

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.chat_page)
        self.stack.addWidget(self.upload_page)
        self.stack.addWidget(self.manage_page)

        self.btn_group.buttonClicked.connect(self.switch_page)
        main_layout.addWidget(self.sidebar_widget)
        main_layout.addWidget(self.stack)

        self.sidebar_widget.hide()
        self.stack.setCurrentIndex(0)

    # ================= 接口逻辑区 =================
    def load_chat_history_list(self):
        self.history_list.clear()
        try:
            res = self.req.get("/api/chat/list")
            if res and res.get("code") == 0:
                for chat in res["data"]["chats"]:
                    cid = chat["chat_id"]
                    title = chat.get('title', f'新对话')

                    item = QListWidgetItem()
                    item.setSizeHint(QSize(0, 40))
                    item.setData(Qt.ItemDataRole.UserRole, cid)
                    self.history_list.addItem(item)

                    # 插入自定义组件（带按钮）
                    widget = ChatListItemWidget(cid, title, self.rename_chat, self.delete_chat)
                    self.history_list.setItemWidget(item, widget)
        except Exception as e:
            print("加载对话列表失败", e)

    def rename_chat(self, chat_id, old_title):
        """重命名对话"""
        new_title, ok = QInputDialog.getText(self, "重命名对话", "请输入新标题:", text=old_title)
        if ok and new_title.strip():
            res = self.req.post(f"/api/chat/rename/{chat_id}", {"title": new_title.strip()})
            if res and res.get("code") == 0:
                self.load_chat_history_list()
            else:
                QMessageBox.warning(self, "错误", res.get("msg", "重命名失败"))

    def delete_chat(self, chat_id):
        """删除对话"""
        reply = QMessageBox.question(self, "确认", "确定彻底删除该对话吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            res = self.req.delete(f"/api/chat/delete/{chat_id}")
            if res and res.get("code") == 0:
                # 如果删掉的是当前正在聊的，清空屏幕
                if self.state["chat_id"] == chat_id:
                    self.state["chat_id"] = None
                    self.chat_page.clear_chat()
                self.load_chat_history_list()
            else:
                QMessageBox.warning(self, "错误", res.get("msg", "删除失败"))

    def switch_history_chat(self, item):
        chat_id = item.data(Qt.ItemDataRole.UserRole)
        self.state["chat_id"] = chat_id

        self.btn_group.setExclusive(False)
        for btn in self.btn_group.buttons():
            btn.setChecked(False)
        self.btn_group.setExclusive(True)

        self.stack.setCurrentIndex(1)
        self.chat_page.load_history()

    def switch_page(self, btn):
        index = self.btn_group.id(btn)
        if not self.state["token"] and index != 0:
            QMessageBox.warning(self, "拦截", "请先登录！")
            return

        if index == 0:
            try:
                res = self.req.post("/api/chat/new", {})
                if res and res.get("code") == 0:
                    self.state["chat_id"] = res["data"]["chat_id"]
                    self.load_chat_history_list()
                    self.chat_page.clear_chat()
            except:
                pass

        self.history_list.clearSelection()
        self.stack.setCurrentIndex(index + 1)

    def login_success(self, username):
        self.user_label.setText(f"👤 {username}")
        self.sidebar_widget.show()
        self.btn_chat.setChecked(True)
        self.load_chat_history_list()
        self.stack.setCurrentIndex(1)

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())