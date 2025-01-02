# -----------------------------------------------------------
# File : options.py
# Author : samellou
# Version : 1.6.0
# Description : Added color options
# -----------------------------------------------------------

from tkinter import *
from tkinter import ttk,colorchooser
from utils import *
import ctypes
from functools import partial
from ctypes import wintypes

#Global variables
button_grid = []
current_grid = possible_input

capture_keycode = 217
capture_keysym = "None"

def open_color(event,color_frame,parent):
    # Ouvrir la boîte de dialogue de couleur
    color = colorchooser.askcolor(parent=parent,title="Choose a color")
    
    if color[1]: 
        color_frame.config(bg=color[1])
 

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


def show_color_menu(window):
    w = Toplevel(window)
    w.wm_title("Color menu")
    w.resizable(width=False,height=False)
    wheight = 200
    wwidth = 500
    w.geometry(f"{wwidth}x{wheight}")


    bold_font = ("Helvetica", 8, "bold")
    
    

    general_label = Label(w,text="General",font=bold_font)
    general_label.place(x = wwidth//6 - 20,y=5)

    face_label = Label(w,text="Face",font=bold_font)
    face_label.place(x = wwidth//2 - 20,y=5)

    hand_label = Label(w,text="Hands",font=bold_font)
    hand_label.place(x = 5*wwidth//6 - 20,y=5)


    sep1 = ttk.Separator(w,orient="vertical")
    sep1.place(x=wwidth//3,y=0,width = 20,height=wheight)

    sep2 = ttk.Separator(w,orient="vertical")
    sep2.place(x=2 * wwidth//3,y=0,width = 20,height=wheight)

    #======================================================

    grid_color_label = Label(w,text="Grid")

    grid_color_height = wheight//8
    padding_col = 20
    grid_color_label.place(x=padding_col,y=grid_color_height)

    global grid_color_frame
    grid_color_frame = Frame(w,height=20,width=20,bg=color_dict["grid_color"],relief="ridge", borderwidth=3)

    
    grid_color_frame.place(x=padding_col + 100,y=grid_color_height)
    grid_color_frame.bind("<Button-1>",lambda event,cf = grid_color_frame,p=w : open_color(event,cf,p))


    #=====================================================

    grid_color_text_label = Label(w,text="Grid text")
    
    grid_color_text_height = wheight//4
    grid_color_text_label.place(x=padding_col,y=grid_color_text_height)

    global grid_text_color_frame
    grid_text_color_frame = Frame(w,height=20,width = 20,bg = color_dict["grid_text_color"],relief="ridge",borderwidth=3)

    grid_text_color_frame.place(x=padding_col+100,y=grid_color_text_height)
    grid_text_color_frame.bind("<Button-1>",lambda event,cf = grid_text_color_frame,p=w : open_color(event,cf,p))

    #=====================================================

    input_color_label = Label(w,text="Current input")
    
    input_color_height =  (3 * wheight)//8
    input_color_label.place(x=padding_col,y=input_color_height)

    global input_color_frame
    input_color_frame = Frame(w,height=20,width = 20,bg = color_dict["input_color"],relief="ridge",borderwidth=3)

    input_color_frame.place(x=padding_col+100,y=input_color_height)
    input_color_frame.bind("<Button-1>",lambda event,cf = input_color_frame,p=w : open_color(event,cf,p))

    #=====================================================

    face_square_label = Label(w,text="Face square")
    face_square_height = wheight//8
    face_square_label.place(x=padding_col + wwidth//3,y=face_square_height)

    global face_square_frame
    face_square_frame = Frame(w,height=20,width = 20,bg = color_dict["face_square_color"],relief="ridge",borderwidth=3)

    face_square_frame.place(x=padding_col + wwidth//3 + 100,y=face_square_height)
    face_square_frame.bind("<Button-1>",lambda event,cf = face_square_frame,p=w : open_color(event,cf,p))

    #=====================================================

    hand_dot_color_label =  Label(w,text="Hand dot")
    hand_dot_height = wheight//8
    hand_dot_color_label.place(x = padding_col + 2 * wwidth//3,y=hand_dot_height)

    global hand_dot_frame
    hand_dot_frame = Frame(w,height=20,width = 20,bg = color_dict["hand_dot_color"],relief="ridge",borderwidth=3)

    hand_dot_frame.place(x=padding_col + 2* wwidth//3 + 100,y=hand_dot_height)
    hand_dot_frame.bind("<Button-1>",lambda event,cf = hand_dot_frame,p=w : open_color(event,cf,p))


    #=====================================================


    hand_ridge_color_label =  Label(w,text="Hand ridge")
    hand_ridge_height = wheight//4
    hand_ridge_color_label.place(x = padding_col + 2 * wwidth//3,y=hand_ridge_height)

    global hand_ridge_frame
    hand_ridge_frame = Frame(w,height=20,width = 20,bg = color_dict["hand_ridge_color"],relief="ridge",borderwidth=3)

    hand_ridge_frame.place(x=padding_col + 2* wwidth//3 + 100,y=hand_ridge_height)
    hand_ridge_frame.bind("<Button-1>",lambda event,cf = hand_ridge_frame,p=w : open_color(event,cf,p))


    #=====================================================

    hand_text_color_label =  Label(w,text="Hand text")
    hand_text_height = 3* wheight//8
    hand_text_color_label.place(x = padding_col + 2 * wwidth//3,y=hand_text_height)

    global hand_text_frame
    hand_text_frame = Frame(w,height=20,width = 20,bg = color_dict["hand_text_color"],relief="ridge",borderwidth=3)

    hand_text_frame.place(x=padding_col + 2* wwidth//3 + 100,y=hand_text_height)
    hand_text_frame.bind("<Button-1>",lambda event,cf = hand_text_frame,p=w : open_color(event,cf,p))


    #=====================================================


    apply_button = Button(w,text="Apply colors",command=lambda cg = grid_color_frame,ctg = grid_text_color_frame,ci = input_color_frame,cfs = face_square_frame,chd=hand_dot_frame,chr=hand_ridge_frame,cht=hand_text_frame : apply_colors(cg,ctg,ci,cfs,chd,chr,cht))
    apply_button_width = (4*wwidth)//5
    apply_button_height = (7*wheight)//8
    apply_button.place(x=apply_button_width,y=apply_button_height - 10)


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

    color_menu_button = Button(t,text = "Color options",command=lambda win=t : show_color_menu(win))
    color_menu_button.place(x=scaled_padx//2 + 55,y=200)




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
    global current_grid, recog_mode,color_dict
    current_grid,recog_mode,frame_limit,color_dict = json.load(open("config.json","r"))

    tks.set(recog_mode)
    rd.set(len(current_grid))
    cd.set(len(current_grid[0]))
    tkf.set(frame_limit)
    draw_grid(canvas,rd.get(),cd.get(),width,height)


def apply_colors(gc,gtc,ic,fsc,hdc,hrc,htc):

    color_dict["grid_color"] = gc.cget("bg")
    color_dict["grid_text_color"] = gtc.cget("bg")
    color_dict["input_color"] = ic.cget("bg")
    color_dict["face_square_color"] = fsc.cget("bg")
    color_dict["hand_dot_color"] = hdc.cget("bg")
    color_dict["hand_ridge_color"] = hrc.cget("bg")
    color_dict["hand_text_color"] = htc.cget("bg")

    with open('config.json', 'r') as f:
        data = json.load(f)
    f.close()

    data[3] = color_dict

    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)
    f.close()


def apply_changes(tks,tkf):
    global recog_mode
    recog_mode = tks.get()
    """Handles config save when you click 'Apply change'"""
    change_possible_input(current_grid)
    with open("config.json","r") as config:
        data = json.load(config)
    config.close()
    with open("config.json","w") as config:
        data[0] = current_grid
        data[1] = tks.get()
        data[2] = tkf.get()
        json.dump(data,config,indent=4)
    config.close()
        