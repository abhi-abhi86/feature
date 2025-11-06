# Broker API Usage Guide

This document provides a template for documenting the specific API endpoints, data formats, and authentication mechanisms for the broker you integrate with the trading agent.

**Broker:** `[Your Broker Name, e.g., Upstox, ICICIdirect Breeze]`

## 1. Authentication

Describe the authentication process. This is often the most complex part.

-   **Method:** (e.g., OAuth 2.0, API Key + Secret)
-   **2FA/TOTP:** (e.g., Does it require a 2FA PIN or TOTP? How is it handled?)
-   **Token Refresh:** (e.g., How often does the access token expire? Is there a refresh token?)

### Example Flow (for a hypothetical OAuth broker):

1.  User is redirected to the broker's login page.
2.  After successful login, the broker redirects back to a `localhost` URL with an `auth_code`.
3.  The application uses the `auth_code` along with the `API_KEY` and `API_SECRET` to request an `access_token`.
4.  The `access_token` is stored in `config/broker_api_keys.env` and used for all subsequent API calls.
5.  The `sebi_compliance.py` module is responsible for refreshing this token before it expires.

## 2. WebSocket API (Live Data)

-   **Endpoint URL:** `[e.g., wss://api.broker.com/v2/feed/instrumentData]`
-   **Connection:** How to establish the connection and authenticate.
-   **Subscription:** How to subscribe to specific instruments (e.g., NIFTY50, RELIANCE).
-   **Data Format:** Provide a sample JSON payload for a live tick.

    ```json
    // Example Tick Data
    {
      "symbol": "NSE_EQ|INE002A01018",
      "ltp": 3500.50,
      "volume": 100000,
      "last_traded_time": 1678886400,
      "bid_price": 3500.40,
      "ask_price": 3500.60
    }
    ```

## 3. REST API (Historical Data & Orders)

Document the key REST endpoints used by the application.

### Get Historical Data

-   **Endpoint:** `/v2/historical-candle-data/...`
-   **Parameters:** `instrument_key`, `interval` (e.g., `1minute`, `day`), `from_date`, `to_date`.
-   **Response Format:** Sample JSON response.

### Place Order

-   **Endpoint:** `/v2/order/place`
-   **Method:** `POST`
-   **Body Parameters:** `instrument_key`, `quantity`, `order_type` (`MARKET`, `LIMIT`), `product` (`D` for delivery, `I` for intraday), `transaction_type` (`BUY`, `SELL`).
-   **Rate Limiting:** As per SEBI guidelines, this must be rate-limited (e.g., max 10 orders per second). This is handled by `sebi_compliance.py`.

### Get Order Status

-   **Endpoint:** `/v2/order/history?order_id={order_id}`
-   **Method:** `GET`
-   **Response Format:** Sample JSON showing an `OPEN`, `FILLED`, or `CANCELLED` order.

## 4. Instrument Identifiers

Explain the format used by the broker to identify tradable instruments.

-   **Format:** (e.g., `EXCHANGE_SEGMENT|TOKEN`)
-   **Examples:**
    -   `NSE_EQ|INE002A01018` for Reliance Industries on NSE.
    -   `NFO_FUT|45678` for a Nifty future contract.

This information is critical for the `data_handler` and `execution_handler` modules to function correctly.
