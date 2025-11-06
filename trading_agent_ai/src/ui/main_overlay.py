from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from .widgets.chat_widget import ChatWidget
from .widgets.plot_widget import PlotWidget
from .widgets.status_widget import StatusWidget

class MainOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Make the main window itself not catch mouse events
        self.central_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self._setup_widgets()

    def _setup_widgets(self):
        # Widgets will be added here
        self.status_widget = StatusWidget()
        self.plot_widget = PlotWidget()
        self.chat_widget = ChatWidget() # Phase 2

        # Add widgets to the layout
        self.layout.addWidget(self.status_widget)
        self.layout.addWidget(self.plot_widget)
        self.layout.addWidget(self.chat_widget)

        # Allow mouse events for the actual widgets
        self.status_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.plot_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.chat_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
