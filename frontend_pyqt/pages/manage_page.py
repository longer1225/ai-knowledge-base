from PyQt6.QtWidgets import *
from PyQt6.QtCore import *



class DocItemWidget(QWidget):
    def __init__(self, doc_id, doc_name, delete_callback):
        super().__init__()
        self.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel(f"📄 {doc_name}")
        name_label.setStyleSheet("font-size: 14px; color: #ECECEC;")

        # 🚨 修复显示不全：放宽尺寸到 85x30，微调 padding
        del_btn = QPushButton("🗑️ 删除")
        del_btn.setFixedSize(85, 30)
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent; color: #FF5555;
                border: 1px solid #FF5555; border-radius: 6px; font-size: 13px;
                padding: 0;
            }
            QPushButton:hover { background-color: #FF5555; color: white; }
        """)
        del_btn.clicked.connect(lambda: delete_callback(doc_id, doc_name))

        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(del_btn)


class ManagePage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        header_layout = QHBoxLayout()
        title = QLabel("📖 知识库文档管理")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        self.refresh_btn = QPushButton("🔄 刷新列表")
        self.refresh_btn.setFixedSize(100, 32)
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.setStyleSheet("""
            QPushButton { background-color: #2A2A2A; color: white; border: 1px solid #444; border-radius: 6px; font-size: 13px; }
            QPushButton:hover { background-color: #383838; border: 1px solid #666; }
        """)
        self.refresh_btn.clicked.connect(self.load)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_btn)

        self.list = QListWidget()
        self.list.setStyleSheet("""
            QListWidget { background-color: transparent; border: none; outline: none; }
            QListWidget::item { background-color: #2A2A2A; border-radius: 8px; padding: 10px 15px; margin-bottom: 10px; }
            QListWidget::item:hover { background-color: #383838; }
            QListWidget::item:selected { background-color: #444444; border-left: 4px solid #FFFFFF; }
        """)

        layout.addLayout(header_layout)
        layout.addWidget(self.list)

    def showEvent(self, event):
        super().showEvent(event)
        if self.main.state.get("token"):
            self.load()

    def load(self):
        self.list.clear()
        self.refresh_btn.setText("⏳ 加载...")
        QApplication.processEvents()

        try:
            res = self.main.req.get("/api/manage")
            docs = res.get("data", [])
            if not docs:
                item = QListWidgetItem("📂 暂无文档")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                self.list.addItem(item)
            else:
                for doc in docs:
                    doc_id = doc.get("doc_id", doc.get("id"))
                    doc_name = doc.get("name", "未知文档")

                    item = QListWidgetItem()
                    item.setSizeHint(QSize(0, 50))  # 给组件足够的高度
                    self.list.addItem(item)
                    custom_widget = DocItemWidget(doc_id, doc_name, self.delete_doc)
                    self.list.setItemWidget(item, custom_widget)
        except:
            pass
        finally:
            self.refresh_btn.setText("🔄 刷新列表")

    def delete_doc(self, doc_id, doc_name):
        reply = QMessageBox.question(
            self, '确认删除', f"确定要彻底删除文档吗？\n\n📄 {doc_name}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # 🚨 修正：你的文档删除路由是 /api/manage/{doc_id}
                res = self.main.req.delete(f"/api/manage/{doc_id}")
                if res.get("code") == 0:
                    self.load()
                else:
                    QMessageBox.warning(self, "失败", res.get("msg", "未知错误"))
            except Exception as e:
                QMessageBox.warning(self, "错误", f"网络异常: {e}")