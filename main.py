import sys
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTextEdit, QPushButton, QProgressBar
)
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QFont

from tools.agent import FootballAgent


class FootballAssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚽ Football Assistant Chat")
        self.setGeometry(350, 150, 900, 700)

        self.agent = FootballAgent()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0D1117;
                color: #E6EDF3;
            }
            QLabel {
                color: #E6EDF3;
            }
            QTextEdit {
                background-color: #161B22;
                color: #E6EDF3;
                border: 1px solid #30363D;
                border-radius: 10px;
                padding: 10px;
                font-size: 15px;
            }
            QPushButton {
                background-color: #238636;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2EA043;
            }
            QProgressBar {
                border: 1px solid #30363D;
                border-radius: 6px;
                text-align: center;
                background-color: #161B22;
            }
        """)

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        title = QLabel("💬 Football Assistant")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display, stretch=1)

        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 0)
        self.loading_bar.hide()
        layout.addWidget(self.loading_bar)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Ask about matches, standings, players, or stats...")
        self.input_box.setFixedHeight(80)
        layout.addWidget(self.input_box)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.handle_user_input)
        layout.addWidget(send_button)

    def handle_user_input(self):
        user_text = self.input_box.toPlainText().strip()
        if not user_text:
            return

        self.chat_display.append(f"🧑‍💻 You: {user_text}")
        self.input_box.clear()

        self.loading_bar.show()

        thread = threading.Thread(target=self.get_ai_response, args=(user_text,))
        thread.start()

    def get_ai_response(self, user_text):
        try:
            ai_response = self.agent.ask(user_text)
        except Exception as e:
            ai_response = f"⚠️ Error: {e}"

        def update_ui():
            self.chat_display.append(f"🤖 Assistant: {ai_response}\n")
            self.loading_bar.hide()

        QApplication.instance().postEvent(self, _FunctionEvent(update_ui))

    def customEvent(self, event):
        if isinstance(event, _FunctionEvent):
            event.execute()


class _FunctionEvent(QEvent):
    EVENT_TYPE = QEvent.Type(QEvent.registerEventType())

    def __init__(self, func):
        super().__init__(self.EVENT_TYPE)
        self.func = func

    def execute(self):
        self.func()


def main():
    app = QApplication(sys.argv)
    window = FootballAssistantGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
