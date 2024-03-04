import depthai as dai
from tracker.parser import get_parser
from tracker.pipeline_setup import create_pipeline, initialize_device
from tracker.utils import get_keys_from_file
from tracker.config import categories


def main():
    try:
        # Parse arguments
        args = get_parser().parse_args()
        # Attempt to read labels to track from file, with exception handling for file read errors
        try:
            list_of_labels = get_keys_from_file('classes.txt', categories)
        except FileNotFoundError:
            print("Classes file not found. Tracking all categories.")
            list_of_labels = [i for i in range(len(categories))]  # Track all if file not found
        # Create the pipeline
        pipeline = create_pipeline(args.full_frame, args.nnPath, list_of_labels)
        conn = dai.DeviceBootloader.getFirstAvailableDevice()
        check = conn[0]
        if not check:
            print("Connect OAK Device")
            check = True
        while check:
            check = initialize_device(pipeline)
    except Exception as e:
        print(f"An error occurred: {e}")
    # print('\nThe results are stored in output.json')


if __name__ == "__main__":
    main()