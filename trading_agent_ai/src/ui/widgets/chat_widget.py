from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal
from ...core.event_bus import event_bus
from ...core.event_types import ChatRequestEvent
from datetime import datetime

class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask about the market...")
        
        self.send_button = QPushButton("Send")
        
        self.layout.addWidget(self.history)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.send_button)
        
        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)

    def send_message(self):
        text = self.input_box.text()
        if text:
            self.add_message("You", text)
            chat_event = ChatRequestEvent(timestamp=datetime.now(), text=text)
            # This needs to be put on the event bus in a thread-safe way
            # from the UI thread. A common pattern is to use a queue
            # that the main asyncio loop is also listening to.
            # For simplicity, we'll assume a direct put for now.
            # In a real app, this would be:
            # asyncio.run_coroutine_threadsafe(event_bus.put(chat_event), loop)
            
            # For this MVP, we'll just print it.
            print(f"UI emitting ChatRequestEvent: {chat_event}")
            self.input_box.clear()

    def add_message(self, sender: str, message: str):
        self.history.append(f"<b>{sender}:</b> {message}")
