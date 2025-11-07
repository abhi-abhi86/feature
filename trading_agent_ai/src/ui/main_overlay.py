from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from .widgets.chat_widget import ChatWidget
from .widgets.plot_widget import PlotWidget
from .widgets.status_widget import StatusWidget
from .widgets.alert_widget import AlertWidget

class MainOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trading Agent AI")
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180);")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self._setup_widgets()

    def _setup_widgets(self):
        self.status_widget = StatusWidget()
        self.plot_widget = PlotWidget()
        self.chat_widget = ChatWidget()
        self.alert_widget = AlertWidget()

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        self.layout.addWidget(self.status_widget)
        self.layout.addWidget(self.plot_widget)
        self.layout.addWidget(self.chat_widget)
        self.layout.addWidget(self.close_button)
