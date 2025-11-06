import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        
        self.plot_widget.setBackground('w')
        self.plot_widget.setTitle("Portfolio Value", color="b", size="20pt")
        styles = {"color": "b", "font-size": "15px"}
        self.plot_widget.setLabel("left", "Value ($)", **styles)
        self.plot_widget.setLabel("bottom", "Time", **styles)
        self.plot_widget.showGrid(x=True, y=True)
        
        self.data_line = self.plot_widget.plot(pen=pg.mkPen(color=(255, 0, 0)))
        self.x_data = []
        self.y_data = []

    def add_point(self, timestamp, value):
        """
        Adds a new point to the P&L chart.
        Timestamp should be a Unix timestamp or similar numeric value.
        """
        self.x_data.append(timestamp)
        self.y_data.append(value)
        self.data_line.setData(self.x_data, self.y_data)
