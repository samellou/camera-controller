# -----------------------------------------------------------
# File : options.py
# Author : samellou
# Version : 1.2.0
# Description : Added Options
# -----------------------------------------------------------

from tkinter import *
from tkinter import ttk
from utils import *
import numpy as np
import ctypes
from ctypes import wintypes
from functools import partial

button_grid = []
current_grid = possible_input

capture_keycode = 217
capture_keysym = "None"


#Save the current assignation to the button
def save_assignation(button1,button2,entry,row,col):
    button1.configure(text=f"{entry.get()}\n({capture_keysym})")
    button2.configure(text=f"{entry.get()}\n({capture_keysym})")
    current_grid[row][col] = [entry.get(),capture_keycode]

#Give an empty grid
def reset_grid(row,col):
    grid = []
    for _ in range(row):
        grid_range = []
        for _ in range(col):
            grid_range.append(["None",217])
        grid.append(grid_range)
    return grid            



# Init Ctypes to get all the VKs
user32 = ctypes.WinDLL('user32', use_last_error=True)


def get_virtual_key_code(window,label,event):
    """Method called to get the vk from an input, with escape as None"""
    vk_code = user32.MapVirtualKeyW(event.keycode, 0)
    label.config(text=f"Button pressed : {event.keysym}")

    global capture_keycode
    global capture_keysym

    if event.keycode == 27:
        capture_keycode = 217
        capture_keysym = "None"
    
    else:
        capture_keycode = event.keycode
        capture_keysym = event.keysym


    window.unbind("<Key>")  # Unbinding the key input


def enable_key_capture(window,label):
    """Method called by a button to capture the first key input"""
    window.focus_set()
    label.config(text="Please press a button\n on your keyboard...")
    
    window.bind("<Key>", partial(get_virtual_key_code, window, label))  # Bind the listener



def get_key_value(vk_code):
    """
    We get the key value of a key input
    """
 
    result = user32.MapVirtualKeyW(vk_code, 0)
    
    if result == 0:
        return None  # If it fails

    # Get unicode
    char = chr(result) if result < 0x10000 else None
    return char



def show_assignation_menu(window,button,row,col):
    """Handles the creation of the assignation menu when you want to map a key"""
    w = Toplevel(window)
    w.wm_title(f"{row},{col}")
    l = Label(w,text=f"Choose input for ({row},{col})")
    l.pack(pady=10)
    l2 = Label(w,text=f"Button name")
    l2.pack(pady=5)
    w.geometry("150x250")

    entry = Entry(w, width=8) 
    entry.pack(pady=2) 

    global capture_keycode
    global capture_keysym

    capture_keycode = 217
    capture_keysym = "None"

    l2 = Label(w,text=f"Input keyboard button")
    l2.pack(pady=5)
    button = Button(w,width=10,height=3)
    button.pack(pady=2)
    l3 = Label(w)
    l3.pack(pady=2)
    button.configure(command= lambda window=w,label=l3 : enable_key_capture(window,label))
    donebutton = Button(w,text="Done",width = 5,height=2,command=lambda b1=button,b2=button_grid[row][col],e=entry,r=row,c=col : save_assignation(b1,b2,e,r,c))
    donebutton.pack(pady=15)




def draw_grid(canvas, rows, cols, width, height):
    """Draws a button grid on the canvas"""
    canvas.delete("all")  # Previous grid deletion

    # Get cells dimension
    cell_width = width / cols
    cell_height = height / rows
    global button_grid
    button_grid = []
    # Add a button range for each rows
    for i in range(rows):
        button_range = []
        for j in range(cols):
            x1 = j * cell_width
            y1 = i * cell_height
            x2 = (j + 1) * cell_width
            y2 = (i + 1) * cell_height

            # Create a button in each cells
            button = Button(canvas, width=10, height=3,text="None\n(None)")
            button.place(x=x1, y=y1, width=cell_width, height=cell_height)
            button.configure(command = lambda button=button,i=i,j=j : show_assignation_menu(canvas,button,i,j))
            button_range.append(button)
        button_grid.append(button_range)



def update_grid(canvas, row_var, col_var, width, height):
    """Updates the grid depending on the sliders"""
    rows = int(row_var)
    cols = int(col_var)
    global current_grid
    current_grid = reset_grid(rows,cols)
    draw_grid(canvas, rows, cols, width, height)




def show_mapping_menu(root):
    """Handles the whole Options window"""
    t= Toplevel(root)
    t.wm_title("Options")
    t.resizable(width=False,height=False)

    row_dim = IntVar(value = len(possible_input))
    col_dim = IntVar(value = len(possible_input[0]))

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    scaled_padx = (screen_width // 2) - (500 // 2)
    scaled_pady = (screen_height // 2) - (300 // 2)

    canvas_width = scaled_padx//3
    canvas_height = scaled_pady//2

    t.geometry(f"{scaled_padx}x{scaled_pady}")
    
    sep = ttk.Separator(t,orient="vertical")
    sep.place(x=scaled_padx//2,y=0,width = 20,height=scaled_pady)

    row_scale = Scale(t,variable=row_dim,orient="horizontal",from_=1,to=8)
    row_scale.place(x=scaled_padx//6,y=(3 * scaled_pady)//4)

    col_scale = Scale(t,variable=col_dim,orient="horizontal",from_=1,to=8)
    col_scale.place(x=scaled_padx//6,y=(7 * scaled_pady)//8)

    canvas = Canvas(t, width=canvas_width, height=canvas_height, bg="white")
    canvas.place(x=scaled_padx//14,y=scaled_pady//8)
    draw_grid(canvas, len(possible_input), len(possible_input[0]), canvas_width, canvas_height)
    for i in range(len(button_grid)):
        for j in range(len(button_grid[0])):
            button = button_grid[i][j]
            button.configure(text=f"{current_grid[i][j][0]}\n({get_key_value(current_grid[i][j][1])})")

    row_scale.configure(command=lambda val : update_grid(canvas,row_var=val,col_var=col_dim.get(),width=canvas_width,height=canvas_height))
    col_scale.configure(command=lambda val : update_grid(canvas,row_var=row_dim.get(),col_var=val,width=canvas_width,height=canvas_height))

    apply_button = Button(t,text="Apply changes",command=apply_changes)
    apply_button.place(x=scaled_padx - 100,y=scaled_pady-50)
    load_button = Button(t,text = "Load config",command=lambda c=canvas,row=row_dim.get(),col=col_dim.get(),w=canvas_width,h=canvas_height,rd=row_dim,cd=col_dim : load_config(c,row,col,w,h,rd,cd))
    load_button.place(x=scaled_padx - 200,y=scaled_pady-50)


def load_config(canvas,row,col,width,height,rd,cd):
    """Handles config load when you press 'Load config'"""
    global current_grid
    current_grid = json.load(open("config.json","r"))
    draw_grid(canvas,row,col,width,height)
    rd.set(len(current_grid))
    cd.set(len(current_grid[0]))




def apply_changes():
    """Handles config save when you click 'Apply change'"""
    #change_possible_input(current_grid)
    with open("config.json","w") as config_file:
        json.dump(current_grid,config_file,indent=4)
        