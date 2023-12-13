import blobconverter
from pathlib import Path

def get_model_path(model_name):
    nn_path = model_name
    if not Path(nn_path).exists():
        print(f"No blob found at {nn_path}. Looking into DepthAI model zoo.")
        nn_path = blobconverter.from_zoo(model_name, shaves=6, zoo_type="depthai", use_cache=True)
    return nn_path
