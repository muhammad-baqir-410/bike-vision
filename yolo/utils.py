import cv2
import numpy as np
import json

# Constants
JSON_INDENT = 2

def frameNorm(frame, bbox):
    normVals = np.full(len(bbox), frame.shape[0])
    normVals[::2] = frame.shape[1]
    return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

def display_frame(name, frame, detections, labels, objects_array):
    color = (255, 0, 0)
    for detection in detections:
        if detection.label in objects_array:
            bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            cv2.putText(frame, labels[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)

    # Show the frame
    cv2.imshow(name, frame)

def get_json_data(detections,object_arrays):

    labels_in_this_frame = {}
    for detection in detections:
        if detection.label in object_arrays:
            if detection.label in labels_in_this_frame.keys():
                labels_in_this_frame[detection.label]+=1
            else:
                labels_in_this_frame[detection.label] = 1
    return labels_in_this_frame

def save_results(results):
    try:
        with open('output.json', 'w') as json_file:
            json.dump(results, json_file, indent=JSON_INDENT)
    except IOError as e:
        print(f"Error saving results to file: {e}")

