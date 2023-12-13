import json
from pathlib import Path
import argparse

def parse_config(config_path):
    path = Path(config_path)
    if not path.exists():
        raise ValueError(f"Path {config_path} does not exist!")

    with path.open() as f:
        return json.load(f)
 

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="Provide model name or model path for inference",
                        default='weights/yolov8n_openvino_2022.1_6shave.blob', type=str)
    parser.add_argument("-c", "--config", help="Provide config path for inference",
                        default='weights/yolov8n.json', type=str)
    return parser.parse_args()


