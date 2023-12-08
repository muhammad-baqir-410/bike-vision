import depthai as dai
import yolo

def main():
    try:
        # Setup and parse configurations
        parser = yolo.parse_arguments()
        config = yolo.parse_config(parser.config)
        nn_path = yolo.get_model_path(parser.model)
        pipeline, labels = yolo.setup_pipeline(config, nn_path)

        with dai.Device(pipeline) as device:
            yolo.process_frames(device, labels)

        print('\nThe results are stored in output.json')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
