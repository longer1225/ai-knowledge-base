from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from frontend_pyqt.stream_thread import StreamThread


class ChatBubble(QWidget):
    def __init__(self, text, is_user=True):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)

        avatar = QLabel("🧑‍💻" if is_user else "🤖")
        avatar.setFont(QFont("Segoe UI Emoji", 18))
        avatar.setFixedSize(35, 35)
        avatar.setAlignment(Qt.AlignmentFlag.AlignTop)

        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        bg_color = "#2F2F2F" if is_user else "transparent"
        bubble.setStyleSheet(f"""
            QLabel {{
                padding: 12px 16px; border-radius: 8px; background-color: {bg_color};
                font-size: 15px; line-height: 1.5; color: #ECECEC;
            }}
        """)

        if is_user:
            layout.addStretch()
            layout.addWidget(bubble)
            layout.addWidget(avatar)
        else:
            layout.addWidget(avatar)
            layout.addWidget(bubble)
            layout.addStretch()

        self.label_ref = bubble
        self.full_text = text


class ChatPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QLabel("💬 AI 知识库问答")
        header.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px; background-color: #212121;")
        layout.addWidget(header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #212121;")
        self.chat_layout = QVBoxLayout(scroll_content)
        self.chat_layout.setContentsMargins(40, 20, 40, 20)
        self.chat_layout.setSpacing(15)
        self.chat_layout.addStretch()
        self.scroll.setWidget(scroll_content)

        # ===== 输入区 =====
        input_container = QWidget()
        input_container.setStyleSheet("background-color: #212121; padding: 20px 40px;")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)

        self.input = QLineEdit()
        self.input.setPlaceholderText("输入你的问题... (按回车发送)")
        self.input.setFixedHeight(50)
        self.input.setStyleSheet("""
            QLineEdit { background-color: #2F2F2F; border: 1px solid #424242; border-radius: 25px; padding: 0 20px; font-size: 15px; }
            QLineEdit:focus { border: 1px solid #5A5A5A; }
        """)
        self.input.returnPressed.connect(self.ask)

        # 只保留下面这 4 行！把 setStyleSheet 删掉！
        self.send_btn = QPushButton("🛫")
        self.send_btn.setObjectName("sendBtn")  # 必须保留这个名字，全局靠它认人！
        self.send_btn.setFixedSize(80, 50)
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.clicked.connect(self.ask)

        input_layout.addWidget(self.input)
        input_layout.addSpacing(10)
        input_layout.addWidget(self.send_btn)

        layout.addWidget(self.scroll)
        layout.addWidget(input_container)

        # 🚨 流式队列平滑渲染控制器
        self.char_queue = []  # 待显示的字符队列
        self.is_typing = False  # 是否正在打字机状态
        self.type_timer = QTimer(self)  # 定时器
        self.type_timer.timeout.connect(self.process_typewriter)

    def scroll_to_bottom(self):
        QTimer.singleShot(50,
                          lambda: self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()))

    def clear_chat(self):
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_history(self):
        self.clear_chat()
        chat_id = self.main.state.get("chat_id")
        if not chat_id: return

        try:
            res = self.main.req.get(f"/api/history/chat/{chat_id}")
            if res and res.get("code") == 0:
                for msg in res.get("data", []):
                    if msg.get("question"):
                        user_b = ChatBubble(msg["question"], is_user=True)
                        self.chat_layout.insertWidget(self.chat_layout.count() - 1, user_b)
                    if msg.get("answer"):
                        ai_b = ChatBubble(msg["answer"], is_user=False)
                        self.chat_layout.insertWidget(self.chat_layout.count() - 1, ai_b)
                self.scroll_to_bottom()
        except Exception as e:
            print("加载历史记录失败", e)

    def ask(self):
        q = self.input.text().strip()
        if not q: return

        self.send_btn.setEnabled(False)
        self.input.clear()

        user_bubble = ChatBubble(q, is_user=True)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, user_bubble)

        # 初始思考提示
        self.current_ai_bubble = ChatBubble("🤔 思考中...", is_user=False)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.current_ai_bubble)
        self.scroll_to_bottom()

        # 🚨 重置打字机状态
        self.is_first_chunk = True
        self.char_queue.clear()
        self.is_typing = True

        self.thread = StreamThread(self.main.req, q, self.main.state["chat_id"])
        self.thread.chunk_signal.connect(self.update_ai)
        self.thread.done_signal.connect(self.finish_ai)
        self.thread.start()

    # ==========================
    # 核心：打字机队列处理
    # ==========================
    def update_ai(self, chunk):
        # 收到数据不直接渲染，而是把字符拆散加入队列！
        if self.is_first_chunk:
            self.current_ai_bubble.full_text = ""
            self.is_first_chunk = False

            # 开启平滑打字机定时器 (数字代表速度：越小越快，越大越慢。15ms 最佳)
            self.type_timer.start(15)

            # 确保 chunk 被转成字符串，并逐字加入队列
        for char in str(chunk):
            self.char_queue.append(char)

    def process_typewriter(self):
        """定时器每 15ms 触发一次，从队列里吐出一个字"""
        if self.char_queue:
            char = self.char_queue.pop(0)
            self.current_ai_bubble.full_text += char
            # 渲染光标
            self.current_ai_bubble.label_ref.setText(self.current_ai_bubble.full_text + " ▌")

            # 定期滚到底部，防止长文本超过屏幕
            if len(self.char_queue) % 5 == 0:
                self.scroll_to_bottom()

        elif not self.is_typing:
            # 当数据全部传完，并且队列也清空了，就关掉定时器
            self.type_timer.stop()
            # 渲染最终无光标版本
            self.current_ai_bubble.label_ref.setText(self.current_ai_bubble.full_text)
            self.send_btn.setEnabled(True)
            self.scroll_to_bottom()
            self.main.load_chat_history_list()

    def finish_ai(self):
        # 后端数据传完了，但可能队列里还有字没打完。改变状态位即可。
        self.is_typing = False