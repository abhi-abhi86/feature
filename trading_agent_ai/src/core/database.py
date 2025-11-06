import sqlite3
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = "local_database/app_data.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database and create tables if they don't exist."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        cursor = self.connection.cursor()

        # Create trades table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT UNIQUE,
                ticker TEXT NOT NULL,
                action TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                timestamp REAL NOT NULL,
                status TEXT DEFAULT 'PENDING'
            )
        ''')

        # Create signals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                action TEXT NOT NULL,
                confidence REAL NOT NULL,
                explanation TEXT,
                timestamp REAL NOT NULL
            )
        ''')

        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_id INTEGER,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp REAL NOT NULL,
                FOREIGN KEY (trade_id) REFERENCES trades (id)
            )
        ''')

        # Create app_logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp REAL NOT NULL
            )
        ''')

        self.connection.commit()
        logger.info("Database initialized successfully.")

    def save_trade(self, trade_data: Dict[str, Any]) -> int:
        """Save a trade to the database."""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO trades (order_id, ticker, action, quantity, price, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            trade_data.get('order_id'),
            trade_data['ticker'],
            trade_data['action'],
            trade_data['quantity'],
            trade_data['price'],
            trade_data['timestamp'],
            trade_data.get('status', 'PENDING')
        ))
        self.connection.commit()
        trade_id = cursor.lastrowid
        logger.info(f"Trade saved with ID: {trade_id}")
        return trade_id

    def get_trade_history(self, ticker: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve trade history, optionally filtered by ticker."""
        cursor = self.connection.cursor()
        if ticker:
            cursor.execute('SELECT * FROM trades WHERE ticker = ? ORDER BY timestamp DESC LIMIT ?', (ticker, limit))
        else:
            cursor.execute('SELECT * FROM trades ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def save_signal(self, signal_data: Dict[str, Any]) -> int:
        """Save a signal to the database."""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO signals (ticker, action, confidence, explanation, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            signal_data['ticker'],
            signal_data['action'],
            signal_data['confidence'],
            signal_data.get('explanation'),
            signal_data['timestamp']
        ))
        self.connection.commit()
        signal_id = cursor.lastrowid
        logger.info(f"Signal saved with ID: {signal_id}")
        return signal_id

    def get_signals(self, ticker: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve signals, optionally filtered by ticker."""
        cursor = self.connection.cursor()
        if ticker:
            cursor.execute('SELECT * FROM signals WHERE ticker = ? ORDER BY timestamp DESC LIMIT ?', (ticker, limit))
        else:
            cursor.execute('SELECT * FROM signals ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def log_event(self, level: str, message: str, timestamp: float):
        """Log an event to the app_logs table."""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO app_logs (level, message, timestamp)
            VALUES (?, ?, ?)
        ''', (level, message, timestamp))
        self.connection.commit()

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed.")
