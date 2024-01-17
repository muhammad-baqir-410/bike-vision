import cv2
import numpy as np
import json
import depthai as dai
from constants import coco_labels
# Constants
JSON_INDENT = 2

def frameNorm(frame, bbox):
    normVals = np.full(len(bbox), frame.shape[0])
    normVals[::2] = frame.shape[1]
    return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

def get_json_data(detections,object_arrays):

    labels_in_this_frame = {}
    for detection in detections:
        if detection.label in object_arrays:
            if detection.label in labels_in_this_frame.keys():
                labels_in_this_frame[detection.label]+=1
            else:
                labels_in_this_frame[detection.label] = 1
    return labels_in_this_frame

def display_frame(name, frame, detections, labels, objects_array):
    color = (255, 0, 0)
    label_counts = get_json_data(detections, objects_array)
    y_start = 30
    for detection in detections:
        if detection.label in objects_array:
            bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            cv2.putText(frame, labels[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            for i, (label, count) in enumerate(label_counts.items()):
                y = y_start + i * 20  # Adjust the increment (20) based on your font size and spacing
                cv2.putText(frame, f'{coco_labels[label]}: {count}', (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

    # Show the frame
    cv2.imshow(name, frame)
    

def save_results(results):
    try:
        with open('output.json', 'w') as json_file:
            json.dump(results, json_file, indent=JSON_INDENT)
    except IOError as e:
        print(f"Error saving results to file: {e}")

def read_coco_classes(file_path):
    try:
        with open(file_path, 'r') as file:
            classes = [line.strip() for line in file]
        return classes
    except IOError as e:
        print(f"Error reading file: {e}")
        return []

def labels_from_coco_classes(file_path):
    # Read the JSON file
    with open('./weights/yolov8n.json', 'r') as file:
        data = json.load(file)
    coco_classes_name = data.get('mappings', {}).get('labels', [])

    # Create a mapping between class names and labels
    coco_given_classes = read_coco_classes(file_path)
    
    coco_class_to_label = {class_name: label for label, class_name in enumerate(coco_classes_name)}
    object_arrays = []
    
    for cls in coco_given_classes:
        class_label = coco_class_to_label.get(cls, -1)
        if class_label != -1:
            object_arrays.append(class_label)
        else:
            print(f"{cls} not found in COCO classes")
                
    return object_arrays
