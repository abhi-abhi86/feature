import pytesseract
import numpy as np
from PIL import Image

def get_ticker_from_image(image: np.ndarray) -> str:
    """
    Uses Tesseract to extract text (assumed to be the ticker) from an image.
    """
    try:
        # Pre-processing can be added here to improve OCR accuracy
        # For example, converting to grayscale, thresholding, etc.
        text = pytesseract.image_to_string(Image.fromarray(image))
        # Clean up the extracted text
        return "".join(filter(str.isalnum, text)).upper()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
