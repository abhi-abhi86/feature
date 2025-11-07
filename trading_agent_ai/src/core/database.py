import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, config, db_path: str = None):
        if db_path is None:
            db_path = config.get("Paths", "database_path", fallback="local_database/app_data.db")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize the database and create tables if they don't exist."""
        cursor = self.conn.cursor()

        # Create trades table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ticker TEXT NOT NULL,
                action TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL NOT NULL,
                order_id TEXT UNIQUE
            )
        ''')

        # Create signals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ticker TEXT NOT NULL,
                signal TEXT NOT NULL,
                confidence REAL,
                reason TEXT
            )
        ''')

        self.conn.commit()
        logger.info("Database initialized successfully.")

    def save_trade(self, trade_data: Dict[str, Any]) -> Optional[int]:
        """Saves a trade to the database."""
        sql = ''' INSERT INTO trades(ticker,action,quantity,price,order_id)
                  VALUES(?,?,?,?,?) '''
        cursor = self.conn.cursor()
        cursor.execute(sql, (
            trade_data.get('ticker'),
            trade_data.get('action'),
            trade_data.get('quantity'),
            trade_data.get('price'),
            trade_data.get('order_id')
        ))
        self.conn.commit()
        logger.info(f"Trade saved with ID: {cursor.lastrowid}")
        return cursor.lastrowid

    def get_trade_history(self, limit: int = 100) -> List[Any]:
        """Retrieves trade history from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM trades ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()

    def save_signal(self, signal_data: Dict[str, Any]) -> Optional[int]:
        """Saves a signal to the database."""
        sql = ''' INSERT INTO signals(ticker,signal,confidence,reason)
                  VALUES(?,?,?,?) '''
        cursor = self.conn.cursor()
        cursor.execute(sql, (
            signal_data.get('ticker'),
            signal_data.get('signal'),
            signal_data.get('confidence'),
            signal_data.get('reason')
        ))
        self.conn.commit()
        logger.info(f"Signal saved with ID: {cursor.lastrowid}")
        return cursor.lastrowid

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()
        logger.info("Database connection closed.")
        
    def initialize(self):
        """Initialize method (for compatibility with main app)."""
        # Already initialized in __init__, this is just for interface compatibility
        logger.info("Database already initialized.")
