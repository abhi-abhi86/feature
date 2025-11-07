from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        
        # Set widget styling
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(50, 50, 50, 180);
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                color: white;
                font-weight: bold;
                padding: 3px 8px;
                border-radius: 3px;
                margin: 2px;
            }
        """)
        
        self.broker_status_label = QLabel("Broker: Disconnected")
        self.news_status_label = QLabel("News: Disconnected")
        self.llm_status_label = QLabel("LLM: N/A")
        
        self.layout.addWidget(self.broker_status_label)
        self.layout.addWidget(self.news_status_label)
        self.layout.addWidget(self.llm_status_label)
        
        self._update_styles()

    def _update_styles(self):
        self.broker_status_label.setStyleSheet("background-color: #CC0000; color: white;")
        self.news_status_label.setStyleSheet("background-color: #CC0000; color: white;")
        self.llm_status_label.setStyleSheet("background-color: #666666; color: white;")

    def update_broker_status(self, is_connected: bool):
        if is_connected:
            self.broker_status_label.setText("Broker: Connected (Demo)")
            self.broker_status_label.setStyleSheet("background-color: #00AA00; color: white;")
        else:
            self.broker_status_label.setText("Broker: Disconnected")
            self.broker_status_label.setStyleSheet("background-color: #CC0000; color: white;")

    def update_news_status(self, is_connected: bool):
        if is_connected:
            self.news_status_label.setText("News: Active")
            self.news_status_label.setStyleSheet("background-color: #00AA00; color: white;")
        else:
            self.news_status_label.setText("News: Error")
            self.news_status_label.setStyleSheet("background-color: #CC0000; color: white;")

    def update_llm_status(self, status: str):
        self.llm_status_label.setText(f"LLM: {status}")
        if status.lower() == 'ok':
            self.llm_status_label.setStyleSheet("background-color: #00AA00; color: white;")
        else:
            self.llm_status_label.setStyleSheet("background-color: #666666; color: white;")
