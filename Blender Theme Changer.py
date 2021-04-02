import tkinter as tk
from tkinter import filedialog, colorchooser
from tkinter import *
import os, sys, ctypes, random, subprocess, time
from colour import Color
from xml.dom import minidom


# Root Settings
root = tk.Tk()
root.title("Blender Color Changer")
root.geometry("400x400")
root.resizable(False, False)
#root.iconwindow = ("Logo.png")


# Main Vars
BlendFilePath = str
BlendColor = [(86, 128, 194)]

# Nodes numbers from Blender Interface settings
InterfaceNodesWithAlpha = [0, 3, 4, 5, 6, 11, 12, 15]
InterfaceNodesWithoutAlpha = [1, 2, 11, 17]


def pickfile():
    # Showing a File dialog for loading the prefrances blend file
    filepath = filedialog.askopenfilename(initialdir="/", title="Theme Preset File",
    filetypes=(("Preset File", "*.xml"), ("all files", "*.*")))

    globals()["BlendFilePath"] = filepath

    # Enabling the Apply button
    Apply["state"] = NORMAL


def pickcolor():
    # Picking the Blender Theme Color
    color = colorchooser.askcolor()

    # Changing the color of the sqaure side to the color buttton
    colorframe.config(bg = '#%02x%02x%02x' % color[0])
    
    globals()["BlendColor"] = color


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
    

    # HEX Color wiithout the alpha value
    SolidColor = '#%02x%02x%02x' % BlendColor[0]
    
    # HEX Color with alpha value
    ListColor = list(BlendColor[0])
    ListColor.append(230)
    TupleColor = tuple(ListColor)
    AlphaColor = '#%02x%02x%02x%02x' % TupleColor

    #---------------------------------------------------------Applying THe Color the theme XML
    for i in InterfaceNodesWithAlpha:
        TWC[i].attributes['inner_sel'].value = AlphaColor

    for i in InterfaceNodesWithoutAlpha:
        TWC[i].attributes['inner_sel'].value = SolidColor
    
    TWC[8].attributes['item'].value = AlphaColor
    
    TUI[0].attributes['widget_text_cursor'].value = SolidColor

    TGE[0].attributes["frame_current"].value = SolidColor

    TDS[0].attributes["frame_current"].value = SolidColor

    TNE[0].attributes["frame_current"].value = SolidColor

    TSE[0].attributes["movie_strip"].value = SolidColor

    TTE[0].attributes["selected_text"].value = SolidColor

    TP[0].attributes["match"].value = SolidColor
    TP[0].attributes["active_modifier"].value = SolidColor

    TO[0].attributes["active"].value = AlphaColor

    TI[0].attributes["info_selected"].value = SolidColor

    TFB[0].attributes["selected_file"].value = SolidColor

    TC[0].attributes["line_output"].value = SolidColor

    TCE[0].attributes["frame_current"].value = SolidColor
    #---------------------------------------------------------Applying THe Color the theme XML

    
    # Saving
    with open(BlendFilePath, "w") as File:
        File.write(theme.toxml())






# Useless Frame
frame = tk.Frame(root, bg = "black")
frame.place(relwidth=1, relheigh=1)

# The Button to pick the userpref blend file
FileButton = tk.Button(root, text="Preset File", padx=5, pady=5, fg="black", bg="white", command=pickfile)
FileButton.place(relwidth=0.5, relheigh=0.2,  relx=0.5, rely=0.15, anchor=tk.CENTER)

# The Button to choose a color
ColorPicker = tk.Button(root, text="Color", padx=5, pady=5, fg="black", bg="white", command=pickcolor)
ColorPicker.place(relwidth=0.3, relheigh=0.2,  relx=0.4, rely=0.5, anchor=tk.CENTER)
#The box on the side of the color button showing the color the user choose
colorframe = tk.Frame(root, bg = '#5680C2')
colorframe.place(relwidth=0.2, relheigh=0.2, relx=0.65, rely=0.5, anchor=tk.CENTER)

Apply = tk.Button(root, text="Apply", padx=5, pady=5, fg="black", bg="white", command=Apply, state=DISABLED)
Apply.place(relwidth=0.5, relheigh=0.2,  relx=0.5, rely=0.85, anchor=tk.CENTER)



root.mainloop()