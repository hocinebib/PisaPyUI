import PySimpleGUI as sg
import os.path

file_list_column = [

    [

        sg.Text("pdb files folder"),

        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),

        sg.FolderBrowse(size=(13, 1)),

    ],

    [
        
        sg.Text(" "*15),

        sg.Listbox(

            values=[], enable_events=True, size=(25, 4), key="-FILE LIST-"

        ),

        sg.Button('Submit folder', size=(13, 1), key='-Submit files-'),

    ],

    [

        sg.Text('Enter pdb id    '), sg.InputText(size=(25, 1), key="-PDB ID-"),
        sg.Button('Submit id', size=(13, 1), key='-Submit id-'),

    ],

]

image_viewer_column = [

    [sg.Text("PisaPy is a Python Wrapper for PDBePISA")],

]

layout = [

    [

        sg.Column(file_list_column),

        sg.VSeperator(),

        sg.Column(image_viewer_column),

    ]

]

# Create the window
window = sg.Window("PisaPy", layout)

# Create an event loop
while True:

    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:

        break


    if event == "-FOLDER-":

        folder = values["-FOLDER-"]

        try:

            # Get list of files in folder

            file_list = os.listdir(folder)

        except:

            file_list = []


        fnames = [

            f

            for f in file_list

            if os.path.isfile(os.path.join(folder, f))

            and f.lower().endswith(".pdb")

        ]

        window["-FILE LIST-"].update(fnames)

    if event == '-Submit id-':
        print(values['-PDB ID-'])
    if event == '-Submit files-':
        print(values['-FILE LIST-'])


window.close()