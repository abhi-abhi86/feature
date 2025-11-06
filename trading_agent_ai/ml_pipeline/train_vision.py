import argparse
from pathlib import Path
import yaml
from ultralytics import YOLO

# Add the project root to the Python path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from trading_agent_ai.src.core.logger import setup_logging

log = setup_logging("train_vision")

def train_vision_model(
    dataset_config: Path,
    epochs: int = 100,
    batch_size: int = 16,
    img_size: int = 640,
    model_variant: str = 'yolov8n.pt',
    output_dir: Path = Path("runs/detect/train")
):
    """
    Trains a YOLOv8 object detection model on chart patterns.

    Args:
        dataset_config (Path): Path to the dataset YAML file.
        epochs (int): Number of training epochs.
        batch_size (int): Batch size for training.
        img_size (int): Image size for training.
        model_variant (str): The base YOLO model variant to use (e.g., 'yolov8n.pt').
        output_dir (Path): Directory to save training runs.
    """
    if not dataset_config.exists():
        log.error(f"Dataset configuration file not found: {dataset_config}")
        return

    log.info(f"Starting YOLOv8 training with model '{model_variant}'...")
    log.info(f"Dataset: {dataset_config}")
    log.info(f"Parameters: Epochs={epochs}, Batch Size={batch_size}, Img Size={img_size}")

    try:
        # Load a pretrained YOLO model
        model = YOLO(model_variant)

        # Train the model
        # The `project` and `name` args determine the output directory.
        model.train(
            data=str(dataset_config),
            epochs=epochs,
            batch=batch_size,
            imgsz=img_size,
            project=output_dir.parent,
            name=output_dir.name,
            exist_ok=True
        )

        log.info("Training completed.")

        # The best model is automatically saved by ultralytics in the output directory
        # under `weights/best.pt`.
        best_model_path = output_dir / "weights" / "best.pt"
        log.info(f"Best model saved at: {best_model_path}")

        # (Optional) You can also export the model to other formats like ONNX
        # model.export(format='onnx')

    except Exception as e:
        log.error(f"An error occurred during model training: {e}", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a YOLOv8 vision model for chart pattern detection.")
    parser.add_argument("--dataset", type=str, default="config/vision_dataset.yaml", help="Path to the dataset configuration YAML file.")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs.")
    parser.add_argument("--batch", type=int, default=16, help="Batch size.")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size.")
    parser.add_argument("--model", type=str, default='yolov8n.pt', help="Base model variant (e.g., yolov8n.pt, yolov8s.pt).")

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    dataset_config_path = project_root / args.dataset
    
    # Define where to save the final model
    # The training run itself will be saved in `runs/detect/train` by default
    # We are just logging the path here for clarity
    output_path = project_root / "runs" / "detect" / "train"

    # --- Create a dummy dataset yaml for demonstration ---
    # In a real scenario, this file would be created by the user.
    if not dataset_config_path.exists():
        log.warning("Dataset YAML not found. Creating a dummy file.")
        dataset_config_path.parent.mkdir(exist_ok=True)
        dummy_yaml_content = {
            'path': str(project_root / 'data' / 'chart_annotations'),
            'train': 'images/train',
            'val': 'images/val',
            'names': {
                0: 'head_and_shoulders',
                1: 'double_top',
                2: 'double_bottom',
                3: 'bullish_flag',
                4: 'bearish_flag'
            }
        }
        with open(dataset_config_path, 'w') as f:
            yaml.dump(dummy_yaml_content, f)
    # -----------------------------------------------------

    train_vision_model(
        dataset_config=dataset_config_path,
        epochs=args.epochs,
        batch_size=args.batch,
        img_size=args.imgsz,
        model_variant=args.model,
        output_dir=output_path
    )

    # The user should then copy the best model to the `models/vision/` directory
    log.info(f"ACTION REQUIRED: Copy the trained model from {output_path / 'weights' / 'best.pt'} to {project_root / 'models' / 'vision' / 'best.pt'} to use it in the main application.")
