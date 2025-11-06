from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt

class AlertWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        self.hide()

    def show_toast(self, message: str, duration: int = 3000):
        self.label.setText(message)
        self.adjustSize()
        # Position it at the bottom-right of the screen (adjust as needed)
        if self.parent():
            parent_rect = self.parent().geometry()
            self.move(parent_rect.right() - self.width() - 10, parent_rect.bottom() - self.height() - 10)
        self.show()
        QTimer.singleShot(duration, self.hide)

    def show_popup(self, message: str, level: str = 'INFO'):
        # A more complex popup could be implemented here, maybe a QDialog
        self.show_toast(f"[{level}] {message}", 5000)
