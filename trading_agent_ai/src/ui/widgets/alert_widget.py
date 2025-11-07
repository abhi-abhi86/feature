from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt

class AlertWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(20, 20, 20, 220);
                color: #00FF00;
                border: 2px solid #00FF00;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)
        self.hide()

    def show_toast(self, message: str, duration: int = 4000):
        self.label.setText(f"🎯 {message}")
        self.adjustSize()
        
        # Position it at the top-right of the screen
        if self.parent():
            parent_rect = self.parent().geometry()
            self.move(parent_rect.right() - self.width() - 20, parent_rect.top() + 20)
        else:
            # Fallback position
            self.move(1200, 50)
            
        self.show()
        self.raise_()
        QTimer.singleShot(duration, self.hide)

    def show_popup(self, message: str, level: str = 'INFO'):
        # Style based on level
        if level == 'ERROR':
            emoji = "❌"
            color = "#FF0000"
        elif level == 'WARNING':
            emoji = "⚠️"
            color = "#FFAA00"
        elif level == 'NEWS':
            emoji = "📰"
            color = "#00AAFF"
        else:
            emoji = "ℹ️"
            color = "#00FF00"
            
        self.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(20, 20, 20, 220);
                color: {color};
                border: 2px solid {color};
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        
        self.show_toast(f"{emoji} [{level}] {message}", 6000)
