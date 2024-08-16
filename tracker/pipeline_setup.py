import depthai as dai
from .config import nnPathDefault, labelMap
from tracker.utils import process_frames, handle_gps, store_data_loop
from gps import send_at_command, find_gps_ports, is_valid_gps_response
import asyncio
import serial
import os

    # Connect to device and start pipeline
async def initialize_device(pipeline):
    """
    Initialize the device and output queues.
    """
    try:
        with dai.Device(pipeline) as device:
            print("Device connected, starting pipeline...")
            preview_queue = device.getOutputQueue("preview", 4, False)
            tracklets_queue = device.getOutputQueue("tracklets", 4, False)

            # Find the correct GPS port dynamically (once)

            # Pass the correct GPS port to the process_frames function
            shared_data = {
                'lat': 0,
                'lon': 0,
                'objects_track_history': {},
                'display': 'DISPLAY' in os.environ
            }

            # Start asynchronous tasks
            task1 = asyncio.create_task(process_frames(preview_queue, tracklets_queue, shared_data))
            task2 = asyncio.create_task(handle_gps("/dev/ttyUSB0", shared_data))
            task3 = asyncio.create_task(store_data_loop(shared_data))

            await asyncio.gather(task1, task2, task3)

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
