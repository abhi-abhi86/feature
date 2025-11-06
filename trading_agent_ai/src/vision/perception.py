import asyncio
import logging
from datetime import datetime
from ultralytics import YOLO

from ..core.event_bus import event_bus
from ..core.event_types import VisionEvent
from ..core.config_loader import ConfigLoader
from . import capture

logger = logging.getLogger(__name__)

class Perception:
    def __init__(self, config: ConfigLoader):
        self.config = config
        model_path = self.config.get("Vision", "yolo_model_path")
        self.model = YOLO(model_path)
        self.screen_region = {
            "left": int(self.config.get("Vision", "screen_region_x")),
            "top": int(self.config.get("Vision", "screen_region_y")),
            "width": int(self.config.get("Vision", "screen_region_width")),
            "height": int(self.config.get("Vision", "screen_region_height")),
        }
        self.active_ticker = None
        self.is_running = False

    def start(self, ticker: str):
        if not self.is_running:
            self.active_ticker = ticker
            self.is_running = True
            asyncio.create_task(self._perception_loop())
            logger.info(f"Vision perception started for ticker {ticker}.")

    def stop(self):
        self.is_running = False
        logger.info("Vision perception stopped.")

    async def _perception_loop(self):
        while self.is_running:
            img = capture.get_screenshot(self.screen_region)
            
            results = self.model.predict(img, stream=False)
            
            for result in results:
                if result.boxes:
                    for box in result.boxes:
                        pattern_name = self.model.names[int(box.cls)]
                        confidence = float(box.conf)
                        
                        if confidence > 0.7: # High confidence filter
                            vision_event = VisionEvent(
                                timestamp=datetime.now(),
                                ticker=self.active_ticker,
                                pattern=pattern_name,
                                confidence=confidence
                            )
                            await event_bus.put(vision_event)
                            logger.debug(f"Detected pattern: {pattern_name} with confidence {confidence}")

            await asyncio.sleep(1) # Run perception once per second
