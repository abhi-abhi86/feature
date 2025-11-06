from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox
from ...core.config_loader import ConfigLoader

class ConfigWidget(QDialog):
    def __init__(self, config_loader: ConfigLoader):
        super().__init__()
        self.config_loader = config_loader
        self.setWindowTitle("Configuration")
        
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        
        self.broker_input = QComboBox()
        self.broker_input.addItems(["upstox", "zerodha", "dummy"]) # Add more brokers
        
        self.rss_feeds_input = QLineEdit()
        
        self.form_layout.addRow("Broker:", self.broker_input)
        self.form_layout.addRow("RSS Feeds:", self.rss_feeds_input)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)
        
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.save_button)
        
        self.load_current_config()

    def load_current_config(self):
        broker = self.config_loader.get("General", "broker", fallback="dummy")
        self.broker_input.setCurrentText(broker)
        
        feeds = self.config_loader.get("General", "rss_feeds", fallback="")
        self.rss_feeds_input.setText(feeds)

    def save_config(self):
        # This is a simplified save. A real implementation would need
        # to write back to the .ini file carefully.
        broker = self.broker_input.currentText()
        feeds = self.rss_feeds_input.text()
        
        print(f"Saving config: Broker={broker}, Feeds={feeds}")
        # self.config_loader.main_config.set("General", "broker", broker)
        # self.config_loader.main_config.set("General", "rss_feeds", feeds)
        # with open(self.config_loader.config_dir / "main_config.ini", 'w') as configfile:
        #     self.config_loader.main_config.write(configfile)
            
        self.accept()
