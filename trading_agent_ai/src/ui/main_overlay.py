from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .widgets.chat_widget import ChatWidget
from .widgets.plot_widget import PlotWidget
from .widgets.status_widget import StatusWidget
from .widgets.alert_widget import AlertWidget

class MainOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        # Make window semi-transparent but not for mouse events
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Set a fixed size and position for better visibility
        self.setGeometry(50, 50, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Set semi-transparent background
        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 200);
                border-radius: 10px;
                color: white;
                font-family: Arial;
                font-size: 12px;
            }
        """)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self._setup_widgets()

    def _setup_widgets(self):
        # Create title
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        title_widget.setStyleSheet("font-size: 16px; font-weight: bold; color: #00FF00;")
        
        # Widgets will be added here
        self.status_widget = StatusWidget()
        self.plot_widget = PlotWidget()
        self.chat_widget = ChatWidget() # Phase 2
        self.alert_widget = AlertWidget() # For notifications

        # Add widgets to the layout
        self.layout.addWidget(self.status_widget)
        self.layout.addWidget(self.plot_widget)
        # Don't add chat widget for now as it's Phase 2
        # self.layout.addWidget(self.chat_widget)
        
        # Make widgets interactive
        self.status_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.plot_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        
        # Set initial window title and styling
        self.setWindowTitle("Trading Agent AI - Live Dashboard")
