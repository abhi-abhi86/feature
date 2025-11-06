import asyncio
from PyQt6.QtCore import QObject, pyqtSignal

from ..core.event_bus import event_bus
from ..core.event_types import PnLUpdateEvent, NewSignalEvent, AlertEvent # Assuming these exist
from .main_overlay import MainOverlay

class UIManager(QObject):
    # Signals to update UI widgets safely from other threads
    pnl_updated = pyqtSignal(float, float)
    new_signal = pyqtSignal(str)
    new_alert = pyqtSignal(str, str)

    def __init__(self, overlay: MainOverlay):
        super().__init__()
        self.overlay = overlay
        self._connect_signals()

    def _connect_signals(self):
        self.pnl_updated.connect(self.overlay.plot_widget.add_point)
        self.new_signal.connect(self.overlay.alert_widget.show_toast)
        self.new_alert.connect(self.overlay.alert_widget.show_popup)

    async def listen_for_ui_events(self):
        """
        Listens on the main event bus for events relevant to the UI.
        """
        while True:
            event = await event_bus.get()
            if isinstance(event, PnLUpdateEvent):
                self.pnl_updated.emit(event.timestamp, event.portfolio_value)
            elif isinstance(event, NewSignalEvent):
                self.new_signal.emit(event.reason)
            elif isinstance(event, AlertEvent):
                self.new_alert.emit(event.message, event.level)
            
            event_bus.task_done()
