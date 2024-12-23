# -----------------------------------------------------------
# File : main.py
# Author : samellou
# Version : 1.0.0
# Description : Whole script to create the camera controller
# -----------------------------------------------------------

# Import needed libs 
import cv2
from pynput.keyboard import Controller,KeyCode


# Grid that defines all the possibles inputs
possible_input = [
    [["A",103],["up",104],["B",105]],
    [["left",100],["neutral",101],["right",102]],
    [["select",97],["down",98],["start",99]]
]



#We define an object of class Controller to handle keyboard inputs
controller = Controller()


def draw_transparent_grid(frame, alpha=0.5):
    """
    Returns the grid that defines input areas.
    
    Parameters
        - frame : An "MatLike" Object from OpenCV that represents a frame captured by your camera
        - alpha : Grid transparency value (low alpha means more transparency)
    Returns:
        - a frame object from OpenCV
    
    """

    #Gets frame dimensions
    height, width, _ = frame.shape

    # Make a copy that will represent the grid overlay 
    overlay = frame.copy()

    # We make a 3x3 grid so we get the dimensions of one square of the grid
    third_width = width // 3
    third_height = height // 3

    # Drawing the lines on the overlay
    for i in range(1, 3):
        # Vertical lines
        cv2.line(overlay, (i * third_width, 0), (i * third_width, height), (0, 0, 255), 2)
        # Horizontal lines
        cv2.line(overlay, (0, i * third_height), (width, i * third_height), (0, 0, 255), 2)

    # For each square we add the input button 
    for row in range(3):
        for col in range(3):
            # Center of each squares
            center_x = (col * third_width) + third_width // 2
            center_y = (row * third_height) + third_height // 2
            text = possible_input[row][col][0]  #The added text is defined by the array "possible_input defined earlier"

            # And we write the text in the middle.
            cv2.putText(overlay, text, (center_x - 20, center_y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

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

# Loading the HaarCascade Computer Vision model for face recog
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Connecting to the default camera of your system.
cap = cv2.VideoCapture(0)


#If you can't open it : we send a little error message
if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la caméra")
    exit()

frame_count = 0  # Frame counter


#Previous input made by the user (we set it to "space" by default)
last_input = input = KeyCode.from_vk(8)


# Like the Ouroboros, we are now stuck within an eternal loop...
while True:
    # We capture a frame
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    
    #If we cannot capture it, we send a image to the console
    if not ret:
        print("Erreur lors de la capture de l'image")
        break

    # To make the face recog easier, let's shade the frame in gray
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # And now the model do its thing.
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # We add the grid to the frame
    frame_with_grid = draw_transparent_grid(frame, alpha=0.5)

    # For each detected faces
    for (x, y, w, h) in faces:
        # We draw a rectangle around it
        cv2.rectangle(frame_with_grid, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Then it gets the position of the detected face in the grid
        height, width, _ = frame.shape
        row, col = get_position_in_grid(x + w // 2, y + h // 2, width, height)

        # Notifying the user about the current position at the top left of the screen might be a good idea
        cv2.putText(frame_with_grid, possible_input[row][col][0], (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        input = KeyCode.from_vk(possible_input[row][col][1])

        #For each two frames
        if frame_count % 2 == 0:
            # If there is a modification of input
            if last_input != input:
                # the previous input is then released 
                if last_input:
                    controller.release(last_input)
                last_input = input

                #and the new input is pressed
                controller.press(input)
        
    
    frame_count += 1

    # Smile to the camera
    cv2.imshow('Camera controller (press "q" to exit)', frame_with_grid)

    # And if you press 'q', say goodbye to the camera
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# And we release the used camera from its burden, and we close the window.
cap.release()
cv2.destroyAllWindows()
