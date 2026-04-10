from PyQt6.QtCore import QThread, pyqtSignal


class StreamThread(QThread):
    chunk_signal = pyqtSignal(str)
    done_signal = pyqtSignal()

    def __init__(self, req, question, chat_id):
        super().__init__()
        self.req = req
        self.question = question
        self.chat_id = chat_id

    def run(self):
        try:
            for chunk in self.req.stream_post(
                    "/api/qa/ask",
                    {"question": self.question, "chat_id": self.chat_id}
            ):
                self.chunk_signal.emit(chunk)

            # 🔥 循环结束后，发出完成信号，通知前端去掉闪烁光标！
            self.done_signal.emit()
        except Exception as e:
            self.chunk_signal.emit(f"\n❌ 请求失败: {str(e)}")
            self.done_signal.emit()