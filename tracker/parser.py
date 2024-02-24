# parser.py
import argparse
from .config import nnPathDefault

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('nnPath', nargs='?', help="Path to mobilenet detection network blob", default=nnPathDefault)
    parser.add_argument('-ff', '--full_frame', action="store_true", help="Perform tracking on full RGB frame", default=False)
    return parser
