import mss
import numpy as np

def get_screenshot(region: dict) -> np.ndarray:
    """
    Captures a screenshot of a specific region of the screen.
    Region is a dict with 'left', 'top', 'width', 'height'.
    """
    with mss.mss() as sct:
        sct_img = sct.grab(region)
        # Convert to a NumPy array
        img = np.array(sct_img)
        # Convert from BGRA to RGB
        img = img[:, :, :3][:, :, ::-1]
        return img
