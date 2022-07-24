import turtle
from tkinter import *
from tkinter import messagebox
import random
import os
import darkdetect
import math
import numpy as np
import time

# public variables
turtle_is_currently_drawing = False
unit_size = 8 # this is the multiplikation factor for the grid, because the turtle moves in pixels but one box on the grid is <unit_size> long and high

# set standard colors appealing to system's colors
if darkdetect.isDark() == True:
    darkmode = True

    button_bg = "#6b00a8"
    background_color = "#262626"
    font_color = "#ffffff"
    textfield_bg = "#181818"
else:
    darkmode = False

    button_bg = "#a543de"
    background_color = "#ededed"
    font_color = "#000000"
    textfield_bg = "#d9d9d9"


# create the main tkinter window
root = Tk()
root.title("Grafikrechner")
root.resizable(0, 0)
root.iconbitmap("Assets/icon/icon.ico")
canvas = Canvas(master=root, width=801, height=801)
root.configure(background=background_color)
canvas.pack()

# Create the turtle screen and put it on the tkinter canvas
turtle_screen = turtle.TurtleScreen(canvas)
turtle_screen.bgpic("Assets/icon/icon.png")
if darkmode == True:
    turtle_screen.bgcolor("#242424")
    turtle_screen.bgpic("Assets/grid4.png")
else:
    turtle_screen.bgcolor("#ffffff")
    turtle_screen.bgpic("Assets/grid3.png")

# Create the turtle (pen)
t = turtle.RawTurtle(turtle_screen)

"""i = 0
punkte = [[0, 0], [4, 2]]
angle = math.atan((punkte[i + 1][1] - punkte[i][1]) / (punkte[i + 1][0] - punkte[i][0]))
distance = math.sqrt((punkte[i + 1][1] - punkte[i][1])**2 + (punkte[i + 1][0] - punkte[i][0])**2)

t.setheading(math.degrees(angle))
t.forward(distance * unit_size)
#t.forward(distance * unit_size)"""



# standard pen attributes and pen colors
darkmode_pen_colors = ["#ff9eea", "#ff5454", "#6b54ff", "#85baff", "#8aff97", "#ff8b33"]
lightmode_pen_colors = ["#08F7FE", "#7122FA", "#14fc14", "#ff8400", "#ff0000"]
t.pensize(2)
t.speed(3)

def check_validity(string_to_be_checked):
    return string_to_be_checked.replace('+', '').replace('-', '').replace('.', '').replace(',', '').isnumeric()

# This method is called if the user presses the "print function" button.
def prepare_function():
    # get the function which the user entered, replace commas with dots and hand it over to the print function
    function = Funktion_Eingabe_Entry.get()
    function = function.replace(",", ".")

    print_function(str(function), Startwert_Entry.get(), Endwert_Entry.get())


def print_function(entered_function, Startwert, Endwert):
    global turtle_is_currently_drawing, unit_size, darkmode
    if turtle_is_currently_drawing == False:
        turtle_is_currently_drawing = True

        if darkmode == True:
            t.pencolor(random.choice(darkmode_pen_colors))
        else:
            t.pencolor(random.choice(lightmode_pen_colors))

        try:
            parabel_positions = []

            if Startwert == "" and Endwert == "":
                for x in np.arange(-240, 240):
                    function = entered_function.replace("x", "*(" + str(x/4) + ")")

                    y = eval(function)
                    if y < 60 and y > -60:
                        parabel_positions.append([x/4, y])
            else:
                for x in range(int(Startwert), int(Endwert)):
                    function = entered_function.replace("x", "*(" + str(x) + ")")
                    y = eval(function)
                    parabel_positions.append([int(x), int(y)])

            print(parabel_positions)
            # go to first location without the pen drawing
            t.penup()
            t.goto(int(parabel_positions[0][0]) * unit_size, int(parabel_positions[0][1]) * unit_size)
            t.pendown()

            #t.speed(0)
            turtle_screen.tracer(0, 50000)

            for i in np.arange(len(parabel_positions)):
                print("test")
                angle = math.atan((parabel_positions[i + 1][1] - parabel_positions[i][1]) / (parabel_positions[i + 1][0] - parabel_positions[i][0]))
                distance = math.sqrt((parabel_positions[i + 1][1] - parabel_positions[i][1]) ** 2 + (parabel_positions[i + 1][0] - parabel_positions[i][0]) ** 2)

                t.setheading(math.degrees(angle))
                t.forward(distance * unit_size)


            t.penup()
            t.goto(0, 0)
            t.pendown()
            turtle_screen.update()
        except:
            pass

        turtle_is_currently_drawing = False


# create and pack control elements
Startwert_Label = Label(root, text="Startwert: ", bg=background_color, fg=font_color).pack(side=LEFT)

Startwert_Entry = Entry(root, bg=textfield_bg, fg=font_color)
Startwert_Entry.pack(side=LEFT)


Endwert_Label = Label(root, text="Endwert: ", bg=background_color, fg=font_color).pack(side=LEFT)

Endwert_Entry = Entry(root, bg=textfield_bg, fg=font_color)
Endwert_Entry.pack(side=LEFT)


Funktion_Eingabe_Label = Label(root, text="Funktion: ", bg=background_color, fg=font_color).pack(side=LEFT)

Funktion_Eingabe_Entry = Entry(root, bg=textfield_bg, fg=font_color)
Funktion_Eingabe_Entry.pack(side=LEFT)


# option menu for selecting the type of function to be drawed
Function_types = [
    "m⋅x",
    "m⋅x+t",
    "a⋅x²+x⋅b+c"
]

variable = StringVar(root)
variable.set(Function_types[0])


Start_Printing_Button = Button(master=root, text="Start printing", command=prepare_function, bg=button_bg, fg=font_color)
Start_Printing_Button.pack(side=RIGHT)

# create tkinter menu bar and it's content
menu_bar = Menu(root)

is_turtle_currently_drawed = True
def change_if_turtle_is_drawed():
    global is_turtle_currently_drawed
    if is_turtle_currently_drawed:
        is_turtle_currently_drawed = False
        t.hideturtle()
    else:
        is_turtle_currently_drawed = True
        t.showturtle()

def clear_canvas():
    if not turtle_is_currently_drawing:
        t.goto(0, 0)
        t.clear()
        t.pendown()
    else:
        messagebox.showinfo("Alert", "Unable to clear the canvas because the turtle is currently drawing!")

preferences = Menu(menu_bar, tearoff=0)
preferences.add_command(label="Enable/Disable pointer", command=change_if_turtle_is_drawed)
preferences.add_command(label="Clear canvas", command=clear_canvas)

style = Menu(menu_bar, tearoff=0)

# add pen_size to style menu bar
pen_size = Menu(menu_bar, tearoff=0)
for unit in range(1, 11):
    pen_size.add_command(label=str(unit), command=lambda: t.pensize(unit))
style.add_cascade(label="Pen size", menu=pen_size)

# add cursor_size to style menu bar
cursor_size = Menu(menu_bar, tearoff=0)
for unit in range(1, 11):
    cursor_size.add_command(label=str(unit), command=lambda: t.shapesize(unit))
style.add_cascade(label="Cursor size", menu=cursor_size)

# add shape selection to style menu bar
shape_selection = Menu(menu_bar, tearoff=0)

shape_selection.add_command(label=str('classic'), command=lambda: t.shape('classic'))
shape_selection.add_command(label=str('turtle'), command=lambda: t.shape('turtle'))
shape_selection.add_command(label=str('circle'), command=lambda: t.shape('circle'))
shape_selection.add_command(label=str('square'), command=lambda: t.shape('square'))
shape_selection.add_command(label=str('triangle'), command=lambda: t.shape('triangle'))
style.add_cascade(label="Cursor shape", menu=shape_selection)

# add the style menu bar to the preferences menu bar
preferences.add_cascade(label="Style", menu=style)

# add the preferences menu bar to the main menu bar
menu_bar.add_cascade(label="Settings", menu=preferences)




about_menu = Menu(menu_bar, tearoff=0)

def open_github():
    os.system("start \"\" https://github.com/WorldOfPaul")

about_menu.add_command(label="GitHub", command=open_github)
menu_bar.add_cascade(label="About", menu=about_menu)

root.config(menu=menu_bar)



root.mainloop()