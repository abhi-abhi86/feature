"""
Database Inspector Tool
Simple GUI tool to view and inspect the SQLite database
"""

import sys
import sqlite3
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QWidget, QTableWidget, QTableWidgetItem, 
                             QComboBox, QPushButton, QHBoxLayout, QLabel)

class DatabaseInspector(QMainWindow):
    def __init__(self, db_path: str):
        super().__init__()
        self.db_path = db_path
        self.setWindowTitle("Trading Agent Database Inspector")
        self.setGeometry(100, 100, 800, 600)
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Controls
        controls_layout = QHBoxLayout()
        self.table_combo = QComboBox()
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        
        controls_layout.addWidget(QLabel("Table:"))
        controls_layout.addWidget(self.table_combo)
        controls_layout.addWidget(refresh_btn)
        controls_layout.addStretch()
        
        # Table display
        self.table_widget = QTableWidget()
        
        layout.addLayout(controls_layout)
        layout.addWidget(self.table_widget)
        
        self.load_tables()
        self.table_combo.currentTextChanged.connect(self.load_table_data)

    def load_tables(self):
        """Load available tables from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            self.table_combo.clear()
            for table in tables:
                self.table_combo.addItem(table[0])
                
            conn.close()
        except Exception as e:
            print(f"Error loading tables: {e}")

    def load_table_data(self, table_name: str):
        """Load data from the selected table."""
        if not table_name:
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Get data
            cursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 100")
            data = cursor.fetchall()
            
            # Populate table widget
            self.table_widget.setColumnCount(len(columns))
            self.table_widget.setHorizontalHeaderLabels(columns)
            self.table_widget.setRowCount(len(data))
            
            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
                    
            conn.close()
        except Exception as e:
            print(f"Error loading table data: {e}")

    def refresh_data(self):
        """Refresh the current table data."""
        current_table = self.table_combo.currentText()
        self.load_table_data(current_table)

def main():
    app = QApplication(sys.argv)
    
    db_path = Path("local_database/app_data.db")
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        print("Please run the main application first to create the database.")
        return
    
    inspector = DatabaseInspector(str(db_path))
    inspector.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
