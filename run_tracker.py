import cv2
import depthai as dai
import time
from pathlib import Path
from tracker.parser import get_parser
from tracker.pipeline_setup import create_pipeline
from tracker.utils import get_keys_from_file, find_unique_class_counts
from tracker.config import categories, nnPathDefault




def main():
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

    # Connect to device and start pipeline
    try:
        with dai.Device(pipeline) as device:
            
            print("Device connected, starting pipeline...")
            # Output queues will be used to get the rgb frames and nn data from the outputs defined above
            preview = device.getOutputQueue("preview", 4, False)
            tracklets = device.getOutputQueue("tracklets", 4, False)

            startTime = time.monotonic()
            counter = 0
            fps = 0
            frame = None
            objects_track_history = {}
            unique_object_count = {}
            # Set the delay for the timer
            interval = 10  # Time interval in seconds (e.g., 5 minutes)
            start_time = time.time()  # Record the start time
            # delay = 5  # 5 minutes
            while(True):
                imgFrame = preview.get()
                track = tracklets.get()
                # print("track:", track)

                counter+=1
                current_time = time.monotonic()
                if (current_time - startTime) > 1 :
                    fps = counter / (current_time - startTime)
                    counter = 0
                    startTime = current_time

                color = (255, 0, 0)
                frame = imgFrame.getCvFrame()
                trackletsData = track.tracklets
                # print("trackletsData: ", trackletsData)

                for t in trackletsData:
                    roi = t.roi.denormalize(frame.shape[1], frame.shape[0])
                    x1 = int(roi.topLeft().x)
                    y1 = int(roi.topLeft().y)
                    x2 = int(roi.bottomRight().x)
                    y2 = int(roi.bottomRight().y)

                    try:
                        label = categories[int(t.label)]
                    except:
                        label = t.label
                    # print("label: ",label,"ID: ",t.id)
                    objects_track_history[t.id] = label
                    cv2.putText(frame, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    cv2.putText(frame, f"ID: {[t.id]}", (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    cv2.putText(frame, t.status.name, (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, cv2.FONT_HERSHEY_SIMPLEX)
                
                unique_object_count = find_unique_class_counts(objects_track_history)
                # print("Unique Objects Count: ", unique_object_count)
                current_time = time.time()
                elapsed_time = current_time - start_time
                if elapsed_time >= interval:
                    # If the specified time has elapsed, process the current state of data
                    print(find_unique_class_counts(objects_track_history))
                    # Reset the start time
                    start_time = time.time()
                cv2.putText(frame, "NN fps: {:.2f}".format(fps), (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color)

                cv2.imshow("tracker", frame)

                if cv2.waitKey(1) == ord('q'):
                    break
            print("Object History track",objects_track_history)
    except Exception as e:
        print(f"Error during device operation: {e}")


if __name__ == "__main__":
    main()
