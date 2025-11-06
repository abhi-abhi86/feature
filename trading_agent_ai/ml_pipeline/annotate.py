import webbrowser
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from trading_agent_ai.src.core.logger import setup_logging

log = setup_logging("annotator")

def open_annotation_tool(tool_name: str = "labelimg"):
    """
    Opens the web page for a recommended image annotation tool.
    """
    urls = {
        "labelimg": "https://github.com/HumanSignal/labelImg",
        "cvat": "https://github.com/opencv/cvat",
        "makesense": "https://www.makesense.ai/"
    }

    url = urls.get(tool_name.lower())

    if url:
        log.info(f"Opening the web page for {tool_name}...")
        webbrowser.open(url)
    else:
        log.error(f"Tool '{tool_name}' not recognized. Available tools: {list(urls.keys())}")

def main():
    """
    Main function to guide the user for data annotation.
    """
    log.info("--- Image Annotation Helper ---")
    log.info("This script helps you get started with annotating your chart images for YOLO model training.")
    log.info("Annotation involves drawing bounding boxes around patterns (e.g., 'bullish_flag') in your images.")
    log.info("The output of these tools should be saved in the 'data/chart_annotations/' directory.")
    log.info("The format should be one .txt file per image, in YOLO format.")
    print("\n") # Add a newline for readability

    log.info("We recommend using one of the following open-source tools:")
    log.info("1. labelImg: A simple, popular desktop application for bounding box annotation.")
    log.info("2. CVAT: A powerful, web-based annotation tool for individuals and teams.")
    log.info("3. Make Sense: A free and simple to use online annotation tool.")
    print("\n")

    try:
        tool_choice = input("Enter the name of the tool you'd like to open (e.g., 'labelImg'): ").strip()
        if tool_choice:
            open_annotation_tool(tool_choice)
        else:
            log.info("No tool selected. Exiting.")
    except KeyboardInterrupt:
        log.info("\nExiting.")

if __name__ == "__main__":
    main()
