import depthai as dai
from .config import nnPathDefault, labelMap
from tracker.utils import process_frames
from gps import send_at_command, find_gps_ports, is_valid_gps_response
import asyncio
import serial

    # Connect to device and start pipeline
def initialize_device(pipeline):
    """
    Initialize the device and output queues.
    """
    try:
        with dai.Device(pipeline) as device:
            print("Device connected, starting pipeline...")
            preview_queue = device.getOutputQueue("preview", 4, False)
            tracklets_queue = device.getOutputQueue("tracklets", 4, False)

            # Find the correct GPS port dynamically (once)
            gps_port = None
            gps_ports = find_gps_ports()

            if gps_ports:
                for port in gps_ports:
                    try:
                        ser_gps = serial.Serial(port, baudrate=115200, timeout=1)
                        print(f"Connected to GPS on {port}")

                        # Send the AT command to get GPS info
                        response = send_at_command(ser_gps, 'AT+CGPSINFO=1')

                        # Check if the response contains valid GPS data
                        if is_valid_gps_response(response):
                            print(f"Successful GPS response from port {port}")
                            gps_port = port
                            break
                        else:
                            print(f"No valid GPS data on port {port}, trying next port...")

                    except Exception as e:
                        print(f"Error connecting to GPS on port {port}: {e}")
                    finally:
                        if 'ser_gps' in locals() and ser_gps.is_open:
                            ser_gps.close()
                            print(f"Closed GPS serial port on {port}.")
            else:
                print("Could not find any matching GPS ports. Please check the connection.")

            # Pass the correct GPS port to the process_frames function
            asyncio.run(process_frames(preview_queue, tracklets_queue, gps_port))

            return False
    except Exception as e:
        print(f"Failed to initialize device and pipeline: {e}")
        initialize_device(pipeline)

def create_pipeline(full_frame_tracking, nn_path=nnPathDefault, label_list=None):
    """
    Creates and configures the DepthAI pipeline.
    
    Parameters:
    - full_frame_tracking (bool): Indicates whether to perform tracking on the full RGB frame.
    - nn_path (str): Path to the neural network model blob.
    - label_list (list): List of labels to track.
    
    Returns:
    - dai.Pipeline: Configured DepthAI pipeline.
    """
    # Create a DepthAI pipeline
    pipeline = dai.Pipeline()

    try:
        # Define sources and outputs
        camRgb = pipeline.create(dai.node.ColorCamera)
        detectionNetwork = pipeline.create(dai.node.MobileNetDetectionNetwork)
        objectTracker = pipeline.create(dai.node.ObjectTracker)

        xlinkOut = pipeline.create(dai.node.XLinkOut)
        trackerOut = pipeline.create(dai.node.XLinkOut)

        xlinkOut.setStreamName("preview")
        trackerOut.setStreamName("tracklets")

        # Camera properties
        camRgb.setPreviewSize(300, 300)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        camRgb.setInterleaved(False)
        camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
        camRgb.setFps(40)

        # Neural Network properties
        detectionNetwork.setBlobPath(nn_path)
        detectionNetwork.setConfidenceThreshold(0.7)
        detectionNetwork.input.setBlocking(False)

        # Object Tracker properties
        if label_list is not None:
            objectTracker.setDetectionLabelsToTrack(label_list)  # Specify labels to track
        else:
            # Default to tracking all available labels
            objectTracker.setDetectionLabelsToTrack([i for i in range(len(labelMap))])
        
        objectTracker.setTrackerType(dai.TrackerType.ZERO_TERM_COLOR_HISTOGRAM)
        objectTracker.setTrackerIdAssignmentPolicy(dai.TrackerIdAssignmentPolicy.UNIQUE_ID)

        # Linking
        camRgb.preview.link(detectionNetwork.input)
        objectTracker.passthroughTrackerFrame.link(xlinkOut.input)

        if full_frame_tracking:
            camRgb.video.link(objectTracker.inputTrackerFrame)
        else:
            detectionNetwork.passthrough.link(objectTracker.inputTrackerFrame)

        detectionNetwork.passthrough.link(objectTracker.inputDetectionFrame)
        detectionNetwork.out.link(objectTracker.inputDetections)
        objectTracker.out.link(trackerOut.input)

    except Exception as e:
        print(f"Error setting up pipeline: {e}")
        raise

    return pipeline
