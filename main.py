import depthai as dai
import yolo


def main():
    try:
        # Setup and parse configurations
        parser = yolo.parse_arguments()
        config = yolo.parse_config(parser.config)
        nn_path = yolo.get_model_path(parser.model)
        pipeline, labels = yolo.setup_pipeline(config, nn_path)
        
        conn = dai.DeviceBootloader.getFirstAvailableDevice()
        check = conn[0]
        if not check:
            print("Connect OAK Device")
            check = True
        while check:
            check = yolo.connection_pipeline(pipeline,labels)
    except Exception as e:

        print(f"An error occurred: {e}")
    print('\nThe results are stored in output.json')

if __name__ == "__main__":
    main()
