# Import necessary libraries
import depthai as dai
from .config import nnPathDefault, labelMap

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
