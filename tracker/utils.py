import cv2
import time
import serial
from tracker.config import categories, nnPathDefault
from datetime import datetime
from gps import is_valid_gps_data, parse_gpgga
from tracker.store_data import store_data
import asyncio
import aiohttp
import os 

def draw_tracklet_info(frame, label, object_id, status, x1, y1, x2, y2):
    """
    Draw tracklet information on the frame.
    """
    cv2.putText(frame, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
    cv2.putText(frame, f"ID: {object_id}", (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
    cv2.putText(frame, status, (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), cv2.FONT_HERSHEY_SIMPLEX)


def process_single_tracklet(t, frame, objects_track_history):
    """
    Process a single tracklet.
    """
    roi = t.roi.denormalize(frame.shape[1], frame.shape[0])
    x1, y1, x2, y2 = int(roi.topLeft().x), int(roi.topLeft().y), int(roi.bottomRight().x), int(roi.bottomRight().y)
    label = categories[int(t.label)] if int(t.label) in categories else t.label
    objects_track_history[t.id] = label
    draw_tracklet_info(frame, label, t.id, t.status.name, x1, y1, x2, y2)


def process_tracklets(tracklets_data, frame,objects_track_history):
    """
    Process each tracklet and update the frame.
    """
    # objects_track_history = {}
    for t in tracklets_data:
        try:
            process_single_tracklet(t, frame, objects_track_history)
        except Exception as e:
            print(f"Failed to process tracklet: {e}")


def get_gps(ser_gps):
    if ser_gps is None:
        return 0, 0
    while True:
        line = ser_gps.readline().decode('ascii', errors='replace').strip()
        # print("line: ", line)
        if line.startswith('$GPGGA'):
            if is_valid_gps_data(line):
                lat, lon = parse_gpgga(line)
                return lat, lon
            else:
                return 0, 0


async def handle_gps(gps_port, shared_data):
    try:
        with serial.Serial(gps_port, baudrate=115200, timeout=1) as ser_gps:
            while True:
                lat, lon = get_gps(ser_gps)
                shared_data['lat'], shared_data['lon'] = lat, lon
                await asyncio.sleep(10)  # Adjust as needed
    except Exception as e:
        print(f"Error reading GPS data: {e}")



async def store_data_loop(shared_data):
    while True:
        current_time = time.time()
        await asyncio.sleep(600)  # 10 minutes interval
        if shared_data['lat'] or shared_data['lon']:
            async with aiohttp.ClientSession() as session:
                await store_data(session, current_time, shared_data['objects_track_history'], shared_data['lat'], shared_data['lon'])
                shared_data['objects_track_history'] = {}



async def process_frames(preview_queue, tracklets_queue, shared_data):
    try:
        while True:
            img_frame_get = preview_queue.get()
            img_frame = img_frame_get.getCvFrame()
            track = tracklets_queue.get()
            tracklets_data = track.tracklets
            process_tracklets(tracklets_data, img_frame, shared_data['objects_track_history'])
            if shared_data['display']:
                cv2.imshow("tracker", img_frame)
                if cv2.waitKey(1) == ord('q'):
                    break
    except Exception as e:
        print(f"Error processing frames: {e}")

def calculate_fps(start_time, counter):
    """
    Calculate and return the current FPS.
    """
    current_time = time.monotonic()
    if (current_time - start_time) > 1:
        fps = counter / (current_time - start_time)
        start_time = current_time
        return current_time, 0, fps  # Reset counter and startTime, return fps
    return start_time, counter, None


def get_key_from_value(d, value):
    for key, val in d.items():
        if val == value:
            return key
    return None


def get_keys_from_file(file_path, categories):
    """
    Reads values from a given text file, one per line, and returns a list of keys
    from the categories dictionary corresponding to those values.
    
    Parameters:
    - file_path (str): The path to the text file containing the values.
    - categories (dict): The dictionary to search for keys based on the values.
    
    Returns:
    - list: A list of keys corresponding to the values read from the file. If a value
            is not found, it is skipped.
    """
    keys = []
    with open(file_path, 'r') as file:
        for line in file:
            value = line.strip()  # Remove any leading/trailing whitespace
            key = get_key_from_value(categories, value)
            if key is not None:
                keys.append(key)
    return keys

