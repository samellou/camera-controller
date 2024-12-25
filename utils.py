# -----------------------------------------------------------
# File : main.py
# Author : samellou
# Version : 1.3.0
# Description : Added Hand tracking
# -----------------------------------------------------------


import cv2
import os
import json
import numpy as np


def euclid_dist(point_a,point_b):
    """Compute the euclidian distance between two points represented as tuples"""
    return np.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)



#Default config
default_input = [
    [["A", 217], ["up", 217], ["B", 217]],
    [["left", 217], ["neutral", 217], ["right", 217]],
    [["select", 217], ["down", 217], ["start", 217]],
]

#If the config file doesn't exist, we create it
if not os.path.exists("config.json"):
    config = open("config.json","w")
    config.write("[\n\t")
    json.dump(default_input,config,indent=4)
    config.write(","+'"Face recog."]')
    config.close()

#We load the config a first time
possible_input,recog_mode = json.load(open("config.json","r"))

#When called, will change the possible inputs to remap
def change_possible_input(array):
    global possible_input
    possible_input = array

def draw_transparent_grid(frame, alpha=0.5):
    """
    Draws a transparent grid with text overlay on the given frame.

    Parameters:
        - frame : A frame object from OpenCV representing the captured frame
        - alpha : Grid transparency value (low alpha means more transparency)
    Returns:
        - A frame object from OpenCV with the grid overlay
    """

    # Reload possible input from the configuration file
    possible_input = json.load(open("config.json", "r"))[0]

    row_len = len(possible_input)
    col_len = len(possible_input[0])

    # Get frame dimensions
    height, width, _ = frame.shape

    # Create a copy for the grid overlay
    overlay = frame.copy()

    # Calculate cell dimensions
    cell_width = width // col_len
    cell_height = height // row_len

    # Draw grid lines on the overlay
    for i in range(1, col_len):
        # Vertical lines
        x = i * cell_width
        cv2.line(overlay, (x, 0), (x, height), (255, 0, 0), 2)

    for j in range(1, row_len):
        # Horizontal lines
        y = j * cell_height
        cv2.line(overlay, (0, y), (width, y), (255, 0, 0), 2)

    # Add text to each cell
    for row in range(row_len):
        for col in range(col_len):
            # Calculate the center of the current cell
            center_x = col * cell_width + cell_width // 2
            center_y = row * cell_height + cell_height // 2

            # Get the text for this cell
            text = possible_input[row][col][0]

            # Calculate text size and baseline
            text_size, _ = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
            )

            # Center the text inside the cell
            text_x = center_x - text_size[0] // 2
            text_y = center_y + text_size[1] // 2

            # Write the text
            cv2.putText(
                overlay,
                text,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2,
            )

    # Merge the overlay with the original frame
    frame_with_grid = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    return frame_with_grid

def get_position_in_grid(face_x, face_y, width, height, row_len, col_len):
    """
    Returns the current position of a detected face in the grid.

    Parameters:
        - face_x : X coordinate of the face
        - face_y : Y coordinate of the face
        - width : width of the grid
        - height : height of the grid
        - row_len : Number of rows in the grid
        - col_len : Number of columns in the grid
    Returns :
        - row : Row of the grid where the face is
        - col : Column of the grid where the face is
    """
    # Cell dimensions
    cell_width = width // col_len
    cell_height = height // row_len

    # Computing cell coordinates
    col = face_x // cell_width
    row = face_y // cell_height

    col = min(col, col_len - 1)
    row = min(row, row_len - 1)

    return round(row), round(col)

def get_landmark_position(landmark,width,height,row_len,col_len):
    """Returns the position of a hand landmark."""
    x = landmark.x
    y = landmark.y

    rel_x = x*width
    rel_y = y*height

    return get_position_in_grid(rel_x,rel_y,width=width,height=height,row_len=row_len,col_len=col_len)


