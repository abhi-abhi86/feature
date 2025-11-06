from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        
        self.broker_status_label = QLabel("Broker: Disconnected")
        self.news_status_label = QLabel("News: Disconnected")
        self.llm_status_label = QLabel("LLM: N/A")
        
        self.layout.addWidget(self.broker_status_label)
        self.layout.addWidget(self.news_status_label)
        self.layout.addWidget(self.llm_status_label)
        
        self._update_styles()

    def _update_styles(self):
        self.broker_status_label.setStyleSheet("color: red;")
        self.news_status_label.setStyleSheet("color: red;")
        self.llm_status_label.setStyleSheet("color: gray;")

    def update_broker_status(self, is_connected: bool):
        if is_connected:
            self.broker_status_label.setText("Broker: Connected")
            self.broker_status_label.setStyleSheet("color: green;")
        else:
            self.broker_status_label.setText("Broker: Disconnected")
            self.broker_status_label.setStyleSheet("color: red;")

    def update_news_status(self, is_connected: bool):
        if is_connected:
            self.news_status_label.setText("News: OK")
            self.news_status_label.setStyleSheet("color: green;")
        else:
            self.news_status_label.setText("News: Error")
            self.news_status_label.setStyleSheet("color: red;")

    def update_llm_status(self, status: str):
        self.llm_status_label.setText(f"LLM: {status}")
        if status.lower() == 'ok':
            self.llm_status_label.setStyleSheet("color: green;")
        else:
            self.llm_status_label.setStyleSheet("color: gray;")
