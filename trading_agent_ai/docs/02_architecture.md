# System Architecture

This document provides a high-level overview of the AI-Powered Trading Agent's architecture. The system is designed as a monolithic desktop application with a modular, event-driven core.

## 1. Core Architectural Blueprint (Monolithic)

The application runs as a single, self-contained process. This simplifies development and deployment for the MVP. The client-server split is deferred for a future cloud-based version.

The architecture is composed of several core modules, each with a distinct responsibility. These modules run concurrently and communicate asynchronously.

![Monolithic Architecture Diagram](./diagrams/monolithic_architecture.png)  <!-- Diagram to be created later -->

### Core Modules:

1.  **Data Handler:** Connects to the broker's API (e.g., Upstox WebSocket) to receive real-time market data (prices, quotes).

2.  **News Handler:** Fetches news headlines from public RSS feeds to provide a stream of "current affairs" data.

3.  **Strategy Handler (The "Alpha Engine"):** This is the brain of the application. It runs the local AI/ML models (YOLOv8 for vision, LSTM-Transformer for prediction) and fuses their outputs with news sentiment to generate trading signals.

4.  **Portfolio & Risk Manager:** Manages the trading account (paper or real), tracks positions, calculates P&L, and enforces risk rules.

5.  **Execution Handler:** The only module authorized to send trade orders to the broker. It manages order lifecycle and ensures regulatory compliance.

6.  **Vision Module:** Captures screen content, performs OCR, and runs the YOLOv8 model to detect chart patterns.

7.  **UI (Overlay):** A transparent PyQt-based overlay that serves as the main user interface for displaying data, alerts, and chat.

## 2. Event-Driven Architecture (EDA)

To prevent blocking operations and ensure a responsive UI, the modules communicate via an internal, asynchronous event bus.

### Event Bus

-   **Implementation:** A simple, in-memory message queue using Python's built-in `asyncio.Queue`.
-   **Function:** It decouples the modules. For example, the `Data Handler` doesn't need to know about the `Strategy Handler`; it simply places a `MarketEvent` onto the bus. Any interested module can then pick it up.

### Event Types

A set of standardized event objects (`dataclasses`) are used for communication, including:

-   `MarketEvent`: New price tick data.
-   `NewsEvent`: A new headline has been fetched.
-   `VisionEvent`: A chart pattern has been detected.
-   `SignalEvent`: The Alpha Engine has generated a trade signal.
-   `OrderRequestEvent`: The Risk Manager has approved a signal for execution.
-   `FillEvent`: An order has been successfully executed.
-   `PnLUpdateEvent`: The P&L has been recalculated.

This event-driven model allows for high cohesion and low coupling, making the system easier to develop, test, and maintain.
