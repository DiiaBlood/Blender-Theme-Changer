from xml.dom import minidom
import tkinter as tk
from tkinter import DISABLED, NORMAL, HORIZONTAL, DoubleVar, colorchooser, filedialog
from colour import Color
from getpass import getuser
from os import path



# Root Settings
root = tk.Tk()
root.title("Blender Theme Changer")
root.geometry("350x500")
root.iconbitmap = ("MCLogo.ico")



# Main Vars
BlendFilePath = str
BlendColor = [(86, 128, 194)]
Shade = "FALSE"
Roundness = 0.4

# Nodes numbers from Blender Interface settings
InterfaceNodesWithAlpha = [0, 3, 5, 6, 13, 11, 15]
InterfaceNodesWithoutAlpha = [1, 2, 17]
NodesWithShading = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19]


def DarkenColor(hex_color, brightness_offset):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
    # hex() produces "0x88", we want just "88"
    return "#" + "".join([hex(i)[2:] for i in new_rgb_int])


def pickfile():
    # Showing a File dialog for loading the prefrances blend file

    # Checks to see if the easiest way to the Blender Config exists
    WinEasyPath = "C:\\Users\\" + getuser() + "\\AppData\\Roaming\\Blender Foundation\\Blender\\"
    
    # Decides if the EasyPath exist then to start with and if it doesn't then go to the pc home folder
    if path.exists(WinEasyPath):
        filepath = filedialog.askopenfilename(initialdir=WinEasyPath, title="Theme Preset File",
        filetypes=(("Preset File", "*.xml"), ("all files", "*.*")))
    else:
        filepath = filedialog.askopenfilename(initialdir="/", title="Theme Preset File",
        filetypes=(("Preset File", "*.xml"), ("all files", "*.*")))

    if filepath != "":
        globals()["BlendFilePath"] = filepath

        # Enabling the Apply button
        Apply["state"] = NORMAL
    else:
        Apply["state"] = DISABLED


def pickcolor():
    # Picking the Blender Theme Color
    color = colorchooser.askcolor()

    # Changing the color of the sqaure side to the color buttton
    if color[0] == None:
        pass
    else:
        colorframe.config(bg = '#%02x%02x%02x' % color[0])
        globals()["BlendColor"] = color


def ShadeSwitch():
    if Shade == "FALSE":
        globals()["Shade"] = "TRUE"
    else:
        globals()["Shade"] = "FALSE"


def RoundenessValue(var=float):
    globals()["Roundness"] = var

def Apply():
# Ge ts the xml file and all of the nodes inside of it for reading and writing the new Preset
    theme = minidom.parse(BlendFilePath)

    TWC = theme.getElementsByTagName('ThemeWidgetColors')
    TUI = theme.getElementsByTagName("ThemeUserInterface")
    TGE = theme.getElementsByTagName("ThemeGraphEditor")
    TDS = theme.getElementsByTagName("ThemeDopeSheet")
    TNE = theme.getElementsByTagName("ThemeNLAEditor")
    TSE = theme.getElementsByTagName("ThemeSequenceEditor")
    TTE = theme.getElementsByTagName("ThemeTextEditor")
    TP = theme.getElementsByTagName("ThemeProperties")
    TO = theme.getElementsByTagName("ThemeOutliner")
    TI = theme.getElementsByTagName("ThemeInfo")
    TFB = theme.getElementsByTagName("ThemeFileBrowser")
    TC = theme.getElementsByTagName("ThemeConsole")
    TCE = theme.getElementsByTagName("ThemeClipEditor")


# Making the Main 4 colors

    # HEX Color wiithout the alpha value
    SolidColor = BlendColor[1]


    # Making a darker version of the same color for more use
    TEMPDarkSolidColor1 = Color(BlendColor[1], luminance=0.4)
    TEMPDarkSolidColor2 = Color(BlendColor[1], luminance=0.2)
    DarkSolidColor = TEMPDarkSolidColor1.hex
    DarkSolidColor2 = TEMPDarkSolidColor2.hex
    
    
    # HEX Color with alpha value
    ListColor = list(BlendColor[0])
    ListColor.append(230)
    TupleColor = tuple(ListColor)
    AlphaColor = '#%02x%02x%02x%02x' % TupleColor

# Applying THe Color the theme XML
    for i in InterfaceNodesWithAlpha:
        TWC[i].attributes['inner_sel'].value = AlphaColor

    for i in InterfaceNodesWithoutAlpha:
        TWC[i].attributes['inner_sel'].value = SolidColor
    
    TWC[8].attributes['item'].value = AlphaColor
    TWC[17].attributes['item'].value = AlphaColor
    
    TUI[0].attributes['widget_text_cursor'].value = DarkSolidColor

    TGE[0].attributes["frame_current"].value = SolidColor

    TDS[0].attributes["frame_current"].value = SolidColor

    TNE[0].attributes["frame_current"].value = SolidColor
    TNE[0].attributes["dopesheet_channel"].value = DarkSolidColor

    TSE[0].attributes["movie_strip"].value = DarkSolidColor

    TTE[0].attributes["selected_text"].value = SolidColor

    TP[0].attributes["match"].value = SolidColor
    TP[0].attributes["active_modifier"].value = SolidColor

    TO[0].attributes["active"].value = DarkSolidColor
    TO[0].attributes["selected_highlight"].value = DarkSolidColor2

    TI[0].attributes["info_selected"].value = DarkSolidColor

    TFB[0].attributes["selected_file"].value = SolidColor

    TC[0].attributes["line_output"].value = SolidColor

    TCE[0].attributes["frame_current"].value = DarkSolidColor


    
# Applying Shading to UI
    for i in NodesWithShading:
        TWC[i].attributes['show_shaded'].value = Shade

# Applying Roundeness to UI
    for i in NodesWithShading:
        TWC[i].attributes['roundness'].value = str(Roundness)

# Saving
    with open(BlendFilePath, "w") as File:
        File.write(theme.toxml())





ButtonColor = "#cccccc"

# Background Frame
BFrame = tk.Frame(root, bg = "#0f1012")
BFrame.place(relwidth=1, relheigh=1)

# The Button to pick the userpref blend file
FileButton = tk.Button(root, text="Preset File", padx=5, pady=5, fg="#1f1466", bg=ButtonColor, command=pickfile)
FileButton.place(relwidth=0.9, relheigh=0.2,  relx=0.5, rely=0.15, anchor=tk.CENTER)

# The Button to Make Blender UI Shaded
ShadeCheckBox = tk.Checkbutton(root, text="Shade", padx=5, pady=5, fg="black", bg=ButtonColor, command=ShadeSwitch)
ShadeCheckBox.place(relwidth=0.9, relheigh=0.12,  relx=0.5, rely=0.325, anchor=tk.CENTER)

# The Button to choose a color
ColorPicker = tk.Button(root, text="Color", padx=5, pady=5, fg="black", bg=ButtonColor, command=pickcolor)
ColorPicker.place(relwidth=0.5, relheigh=0.2,  relx=0.3, rely=0.5, anchor=tk.CENTER)
#The box on the side of the color button showing the color the user choose
colorframe = tk.Frame(root, bg = '#5680C2')
colorframe.place(relwidth=0.4, relheigh=0.2, relx=0.75, rely=0.5, anchor=tk.CENTER)

# The Value of Blenders UI Roundness
scale_var = DoubleVar()
scale_var.set(0.4)
RoundValueBox = tk.Scale(root, fg="black", bg=ButtonColor, command=RoundenessValue, orient=HORIZONTAL, from_=0, to=1, resolution=0.01, variable=scale_var)
RoundValueBox.place(relwidth=0.9, relheigh=0.12,  relx=0.5, rely=0.6725, anchor=tk.CENTER)

Apply = tk.Button(root, text="Apply", padx=5, pady=5, fg="black", bg=ButtonColor, command=Apply, state=DISABLED)
Apply.place(relwidth=0.9, relheigh=0.2,  relx=0.5, rely=0.85, anchor=tk.CENTER)



root.mainloop()