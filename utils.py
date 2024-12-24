# -----------------------------------------------------------
# File : main.py
# Author : samellou
# Version : 1.1.0
# Description : Camera controller utility functions
# -----------------------------------------------------------


import cv2

possible_input = [
    [["A", 103], ["up", 104], ["B", 105]],
    [["left", 100], ["neutral", 101], ["right", 102]],
    [["select", 97], ["down", 98], ["start", 99]],
]

def modify_possible_input(row,col,input_name,input_value):
    """
    To be continued...
    """
    modified_inputs = possible_input
    modified_inputs[row][col] = [input_name,input_value]
    return modified_inputs



def draw_transparent_grid(frame, alpha=0.5):
    """
    Returns the grid that defines input areas.

    Parameters
        - frame : An "MatLike" Object from OpenCV that represents a frame captured by your camera
        - alpha : Grid transparency value (low alpha means more transparency)
    Returns:
        - a frame object from OpenCV

    """

    # Gets frame dimensions
    height, width, _ = frame.shape

    # Make a copy that will represent the grid overlay
    overlay = frame.copy()

    # We make a 3x3 grid so we get the dimensions of one square of the grid
    third_width = width // 3
    third_height = height // 3

    # Drawing the lines on the overlay
    for i in range(1, 3):
        # Vertical lines
        cv2.line(
            overlay, (i * third_width, 0), (i * third_width, height), (255, 0, 0), 2
        )
        # Horizontal lines
        cv2.line(
            overlay, (0, i * third_height), (width, i * third_height), (255, 0, 0), 2
        )

    # For each square we add the input button
    for row in range(3):
        for col in range(3):
            # Center of each squares
            center_x = (col * third_width) + third_width // 2
            center_y = (row * third_height) + third_height // 2
            text = possible_input[row][col][
                0
            ]  # The added text is defined by the array "possible_input defined earlier"

            # And we write the text in the middle.
            cv2.putText(
                overlay,
                text,
                (center_x - 20, center_y + 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2,
            )

    # Then we fuse the 2 overlays (classic frame and the overlay copy)
    frame_with_grid = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    return frame_with_grid

def get_position_in_grid(face_x, face_y, width, height):
    """
    Returns the current position of a detected face in the grid.

    Parameters:
        - face_x : X coordinate of the face
        - face_y : Y coordinate of the face
        - width : width of the face
        - height : height of the face
    Returns :
        - row : Row of the grid where the face is
        - col : Column of the grid where the face is

    """
    third_width = width // 3
    third_height = height // 3

    col = face_x // third_width
    row = face_y // third_height

    return row, col
