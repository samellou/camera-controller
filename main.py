# -----------------------------------------------------------
# File : main.py
# Author : samellou
# Version : 1.2.0
# Description : Added Options
# -----------------------------------------------------------

from pynput.keyboard import Controller, KeyCode
import mediapipe as mp
import keyboard
from options import *
from PIL import Image, ImageTk



# Capture init
controller = Controller()
capture_enabled = False
cap = cv2.VideoCapture(0)

# Mediapipe Face Detection Model
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Global variables
frame_count = 0
last_input = None

# Function to toggle capture mode
def toggle_capture():
    global capture_enabled
    capture_enabled = not capture_enabled

def show_map():
    global root
    show_mapping_menu(root)


# TKinter init
root = Tk()
root.title("Camera Controller")
root.resizable(width=False, height=False)

# Menu
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Activate/Deactivate capture    P", command=toggle_capture)
file_menu.add_command(label="Options", command=show_map)
menu_bar.add_cascade(label="Menu", menu=file_menu)
root.config(menu=menu_bar)

# Video Label
video_label = Label(root)
video_label.pack()

# Video Update function
def update_video():
    """
    Handles the camera output in general
    
    """
    global frame_count, last_input

    ret, frame = cap.read()
    if not ret or not cap.isOpened():
        print("Erreur : Impossible de capturer la vidéo.")
        root.after(10, update_video)
        return
    
    

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)  # Flip horizontal
    frame_with_grid = draw_transparent_grid(frame)

    # When the capture is enabled :
    if capture_enabled:
        possible_input = json.load(open("config.json","r"))
        row_len = len(possible_input)
        col_len = len(possible_input[0])
        
        # Let's use mediapipe
        results = face_detection.process(frame)
        
        #For each detections if there is at least one :
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                # Draw a rectangle on the face
                cv2.rectangle(frame_with_grid, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Get the face position in the grid
                height, width, _ = frame.shape
                row, col = get_position_in_grid(x + w // 2, y + h // 2, width, height,row_len = row_len, col_len = col_len)        
                print(row,col)
                # Show where we are
                cv2.putText(
                    frame_with_grid,
                    possible_input[row][col][0],
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

                # Keyboard input
                
                input = KeyCode.from_vk(possible_input[row][col][1])
                if frame_count % 2 == 0 and input and last_input != input:
                    if last_input:
                        controller.release(last_input)
                    last_input = input
                    controller.press(input)
            

        frame_count += 1
    else:
        frame_with_grid = frame  # Then the capture will be normal

    # Output
    img = ImageTk.PhotoImage(Image.fromarray(frame_with_grid))
    video_label.config(image=img)
    video_label.image = img

    #Shortcut for capture/activation
    if keyboard.is_pressed("p"):
        toggle_capture()
    # Every 1 ms we update the video
    root.after(1, update_video)

# We call the update_video function to begin the capture
update_video()

# TKinter main loop
root.mainloop()

# Free the camera and close windows
cap.release()
cv2.destroyAllWindows()