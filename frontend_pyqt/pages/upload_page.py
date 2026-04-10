from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import requests

from backend.config import API_BASE_URL


class UploadPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        # 全局居中布局
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ================= 核心：居中的上传卡片 =================
        self.card = QWidget()
        self.card.setFixedSize(500, 350)
        self.card.setObjectName("upload_card")
        self.card.setStyleSheet("""
            QWidget#upload_card {
                background-color: #2A2A2A;
                border: 2px dashed #555555;
                border-radius: 15px;
            }
            QWidget#upload_card:hover {
                border: 2px dashed #888888;
                background-color: #2F2F2F;
            }
        """)

        card_layout = QVBoxLayout(self.card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setSpacing(20)

        # 1. 图标
        icon_label = QLabel("📤")
        icon_label.setFont(QFont("Segoe UI Emoji", 48))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background: transparent; border: none;")

        # 2. 标题
        title_label = QLabel("上传知识库文档")
        title_label.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: white; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 3. 副标题
        sub_label = QLabel("支持 .txt, .docx, .pdf 等格式 (单文件建议 < 20MB)")
        sub_label.setStyleSheet("font-size: 14px; color: #888888; background: transparent; border: none;")
        sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 4. 上传按钮
        self.btn = QPushButton("选择文件上传")
        self.btn.setFixedSize(200, 45)
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF; color: #000000;
                font-weight: bold; border-radius: 8px; font-size: 16px;
                border: none;
            }
            QPushButton:hover { background-color: #E0E0E0; }
            QPushButton:disabled { background-color: #555555; color: #888888; }
        """)
        self.btn.clicked.connect(self.upload)

        # 组装卡片
        card_layout.addStretch()
        card_layout.addWidget(icon_label)
        card_layout.addWidget(title_label)
        card_layout.addWidget(sub_label)
        card_layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        card_layout.addStretch()

        main_layout.addWidget(self.card)

    def upload(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择要上传的文档", "", "All Files (*)")
        if not path:
            return

        # UI 反馈：正在上传
        self.btn.setEnabled(False)
        self.btn.setText("⏳ 上传并处理中...")
        QApplication.processEvents()  # 强制立刻刷新UI

        try:
            with open(path, "rb") as f:
                files = {"file": f}
                res = requests.post(
                    API_BASE_URL + "/api/upload",
                    headers={"Authorization": f"Bearer {self.main.state['token']}"},
                    files=files
                )

            if res.status_code == 200:
                QMessageBox.information(self, "成功", "✅ 文档上传并处理完成！")
            else:
                QMessageBox.warning(self, "失败", f"上传失败，状态码: {res.status_code}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"发生错误：\n{str(e)}")
        finally:
            # 恢复按钮状态
            self.btn.setEnabled(True)
            self.btn.setText("选择文件上传")