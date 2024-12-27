# -----------------------------------------------------------
# File : options.py
# Author : samellou
# Version : 1.5.0
# Description : Corrected some UI issues
# -----------------------------------------------------------

from tkinter import *
from tkinter import ttk
from utils import *
import ctypes
from functools import partial
from ctypes import wintypes

#Global variables
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
 
  # buffer for the char
    buffer = ctypes.create_unicode_buffer(2)
    
    if user32.ToUnicode(vk_code, 0, ctypes.pointer((wintypes.BYTE * 256)()), buffer, len(buffer), 0) > 0:
        return buffer.value  # get unicode character
    else:
        return None 


def show_assignation_menu(window,button,row,col):
    """Handles the creation of the assignation menu when you want to map a key"""
    w = Toplevel(window)
    w.wm_title(f"{row},{col}")
    l = Label(w,text=f"Choose input for ({row},{col})")
    l.pack(pady=10)
    l2 = Label(w,text=f"Button name")
    l2.pack(pady=5)
    w.geometry("150x300")

    entry = Entry(w, width=8)
    entry.insert(0, button.cget("text").split("\n")[0])  
    entry.pack(pady=2) 

    global capture_keycode
    global capture_keysym

    capture_keycode = 217
    capture_keysym = "None"

    l2 = Label(w,text=f"Input keyboard button")
    l2.pack(pady=5)
    button = Button(w,width=10,height=3,text="cu")
    button.pack(pady=2)
    button.configure(text=f"{current_grid[row][col][0]}\n({get_key_value(current_grid[row][col][1])})")
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
            button = Button(canvas, width=10, height=3,text=f"{current_grid[i][j][0]}\n({get_key_value(current_grid[i][j][1])})")
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

    tk_recog_mode = StringVar(value = recog_mode)
    tk_frame_limit = IntVar(value= frame_limit)


    row_dim = IntVar(value = len(possible_input))
    col_dim = IntVar(value = len(possible_input[0]))

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    scaled_padx = (screen_width // 2) - (500 // 2)
    scaled_pady = (screen_height // 2) - (300 // 2) + 50

    
    canvas_width = scaled_padx//3
    canvas_height = scaled_pady//2

    t.geometry(f"{scaled_padx}x{scaled_pady}")
    
    sep = ttk.Separator(t,orient="vertical")
    sep.place(x=scaled_padx//2,y=0,width = 20,height=scaled_pady)

    row_scale = Scale(t,variable=row_dim,orient="horizontal",from_=1,to=8)
    row_scale.place(x=scaled_padx//6,y=(3 * scaled_pady)//4)
    row_l = Label(t,text="Rows : ")
    row_l.place(x=row_scale.winfo_x() + 50,y= (3 * scaled_pady)//4 + 18)

    col_scale = Scale(t,variable=col_dim,orient="horizontal",from_=1,to=8)
    col_scale.place(x=scaled_padx//6,y=(7 * scaled_pady)//8 - 20)
    col_l = Label(t,text="Columns : ")
    col_l.place(x=col_scale.winfo_x() + 45,y= (7 * scaled_pady)//8 -3)

    canvas = Canvas(t, width=canvas_width, height=canvas_height, bg="white")
    canvas.place(x=scaled_padx//14,y=scaled_pady//8)

    l = Label(t,text="Click on a button of this grid to change its mapping.")
    l.place(x=canvas.winfo_x() + 30,y=canvas.winfo_y()+10)

    recog_options = ["Face recog.","Hand recog."]

    dropdown_label = Label(t,text = "Select a recognition mode :")
    dropdown_label.place(x=scaled_padx//2 + 45, y = 30)

    dropdown = OptionMenu(t,tk_recog_mode, *recog_options)
    dropdown.place(x=scaled_padx//2 + 50, y = 50)


    frame_limit_label = Label(t,text = "Select input frame frequency :")
    frame_limit_label.place(x=scaled_padx//2 + 45, y = 90)

    frame_limit_scale = Scale(t,variable=tk_frame_limit,orient="horizontal",from_=1,to=100,length=scaled_padx//3)
    frame_limit_scale.place(x=scaled_padx//2 + 50, y = 120)






    draw_grid(canvas, len(possible_input), len(possible_input[0]), canvas_width, canvas_height)
    for i in range(len(button_grid)):
        for j in range(len(button_grid[0])):
            button = button_grid[i][j]
            button.configure(text=f"{current_grid[i][j][0]}\n({get_key_value(current_grid[i][j][1])})")

    row_scale.configure(command=lambda val : update_grid(canvas,row_var=val,col_var=col_dim.get(),width=canvas_width,height=canvas_height))
    col_scale.configure(command=lambda val : update_grid(canvas,row_var=row_dim.get(),col_var=val,width=canvas_width,height=canvas_height))

    apply_button = Button(t,text="Apply changes",command=lambda tks=tk_recog_mode,tkf=tk_frame_limit : apply_changes(tks,tkf))
    apply_button.place(x=scaled_padx - 100,y=scaled_pady-50)
    load_button = Button(t,text = "Load config",command=lambda c=canvas,w=canvas_width,h=canvas_height,rd=row_dim,cd=col_dim,tks= tk_recog_mode,tkf = tk_frame_limit : load_config(c,w,h,rd,cd,tks,tkf))
    load_button.place(x=scaled_padx - 200,y=scaled_pady-50)

def load_config(canvas,width,height,rd,cd,tks,tkf):
    """Handles config load when you press 'Load config'"""
    global current_grid, recog_mode
    current_grid,recog_mode,frame_limit = json.load(open("config.json","r"))

    tks.set(recog_mode)
    rd.set(len(current_grid))
    cd.set(len(current_grid[0]))
    tkf.set(frame_limit)
    draw_grid(canvas,rd.get(),cd.get(),width,height)


def apply_changes(tks,tkf):
    """Handles config save when you click 'Apply change'"""
    change_possible_input(current_grid)
    with open("config.json","w") as config:
        config.write("[\n\t")
        json.dump(current_grid,config,indent=4)
        config.write(","+f'"{tks.get()}",{tkf.get()}]')
        config.close()
        
    global recog_mode
    recog_mode = tks.get()
        