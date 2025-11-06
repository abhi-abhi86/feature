import requests
import logging
from typing import Any, Dict, Optional

from ..core.config_loader import ConfigLoader

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.base_url = self.config.get("Broker", "rest_url")
        self.api_key = self.config.get("Broker", "api_key")
        self.api_secret = self.config.get("Broker", "api_secret")
        self.timeout = self.config.get_main_config("API", "timeout", fallback=30)
        self.headers = {
            'Accept': 'application/json',
            # Add other necessary headers, e.g., for authentication
        }

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, params=params, json=data, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise

    def get_historical_data(self, ticker: str, interval: str, from_date: str, to_date: str) -> Any:
        """
        Fetches historical data for a given ticker.
        The endpoint and parameters are broker-specific.
        """
        endpoint = f"/historical-data/{ticker}"
        params = {
            "interval": interval,
            "from": from_date,
            "to": to_date
        }
        return self._request("GET", endpoint, params=params)

    def get_account_balance(self) -> Any:
        """
        Fetches the account balance.
        """
        endpoint = "/user/balance"
        return self._request("GET", endpoint)

    def get_order_status(self, order_id: str) -> Any:
        """
        Fetches the status of a specific order.
        """
        endpoint = f"/orders/{order_id}"
        return self._request("GET", endpoint)

    def place_order(self, order_details: Dict) -> Any:
        """
        Places a new order.
        """
        endpoint = "/orders"
        return self._request("POST", endpoint, data=order_details)
