import cv2
import time
import json
from datetime import datetime
from yolo.utils import display_frame, get_json_data, save_results,labels_from_coco_classes

WHITE_COLOR = (255, 255, 255)
FRAME_SHAPE_Y_POSITION = -4
FONT_SCALE = 0.4
RGB_WINDOW = "rgb"
SECONDS_INFER = 1
KEY_QUIT = 'q'
PATH_TO_CLASSES = './classes.txt'

def update_frame_and_detections(q_rgb, q_det, frame, detections, counter, start_time):
    in_rgb = q_rgb.tryGet()
    in_det = q_det.tryGet()

    if in_rgb is not None:
        frame = in_rgb.getCvFrame()
        cv2.putText(frame, f"NN fps: {counter / (time.monotonic() - start_time):.2f}",
                    (2, frame.shape[0] + FRAME_SHAPE_Y_POSITION), cv2.FONT_HERSHEY_TRIPLEX, FONT_SCALE, WHITE_COLOR)

    if in_det is not None:
        detections = in_det.detections
        counter += 1

    return frame, detections, counter
# You can add other utility functions here as needed

def process_frames(device, labels):
    q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    q_det = device.getOutputQueue(name="nn", maxSize=4, blocking=False)

    frame = None
    detections = []
    start_time = time.monotonic()
    counter = 0
    start_time_infer = time.time()
    try:
        with open('output.json', 'r') as file:
            results = json.load(file)
    except:
        with open('output.json', 'w') as file:
            results = json.dump({},file)

    # objects_array = [0, 39]
    objects_array = labels_from_coco_classes(PATH_TO_CLASSES)

    while True:
        frame, detections, counter = update_frame_and_detections(q_rgb, q_det, frame, detections, counter, start_time)

        if frame is not None:
            display_frame(RGB_WINDOW, frame, detections, labels, objects_array)

        current_time = time.time()
        if current_time - start_time_infer >= SECONDS_INFER:
            frame_result = get_json_data(detections, objects_array)
            start_time_infer = current_time
            results[datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')] = frame_result
            save_results(results)
        if cv2.waitKey(1) == ord(KEY_QUIT):
            break


