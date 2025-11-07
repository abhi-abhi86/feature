import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # Add a title label
        self.title_label = QLabel("Live Portfolio Value")
        self.title_label.setStyleSheet("""
            color: #00FF00;
            font-size: 14px;
            font-weight: bold;
            text-align: center;
            padding: 5px;
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        
        # Style the plot
        self.plot_widget.setBackground('#2D2D30')
        self.plot_widget.setTitle("Portfolio Performance", color="w", size="12pt")
        styles = {"color": "#FFFFFF", "font-size": "10px"}
        self.plot_widget.setLabel("left", "Value ($)", **styles)
        self.plot_widget.setLabel("bottom", "Time", **styles)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        # Set plot line style
        pen = pg.mkPen(color='#00FF00', width=2)
        self.data_line = self.plot_widget.plot(pen=pen)
        
        self.x_data = []
        self.y_data = []
        
        # Set a minimum size
        self.setMinimumSize(400, 300)

    def add_point(self, timestamp, value):
        """
        Adds a new point to the P&L chart.
        Timestamp should be a Unix timestamp or similar numeric value.
        """
        self.x_data.append(timestamp)
        self.y_data.append(value)
        
        # Keep only last 100 points for performance
        if len(self.x_data) > 100:
            self.x_data = self.x_data[-100:]
            self.y_data = self.y_data[-100:]
        
        self.data_line.setData(self.x_data, self.y_data)
        
        # Update title with current value
        self.title_label.setText(f"Live Portfolio Value: ${value:,.2f}")
