#!/usr/bin/python3
"""
The graphical user interface of PisaPy

  How to use
  ----------
First you need to have the python packages 

Then you can run the script with the following command :

    python 

  Author
  ------
    Hocine Meraouna

"""
import tkinter as tk
import PySimpleGUI as sg
import os.path
import RunPisaPy as rppy


def create_layouts():
    """
    """
    sg.theme('SystemDefaultForReal')
    ttk_style = 'alt'
    sg.change_look_and_feel('DarkBlue')

    tab1 = [

        [sg.Text("\n"),
         sg.Text("Naccess bin path  "),
         sg.In(size=(25, 1), enable_events=True, key="-FOLDER1-"),
         sg.FolderBrowse(size=(11, 1)),],

        [sg.Text("  pdb files folder  "),
         sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
         sg.FolderBrowse(size=(11, 1)),],

        [sg.Text(" "*20),
         sg.Listbox(values=[], enable_events=True, size=(23, 4), key="-FILE LIST-"),],

        [sg.Text('\n'),
         sg.Text('pdb ID            '), sg.InputText(size=(25, 1), key="-PDB ID-"),],

        [sg.Text("  result storing dir"),
         sg.In(size=(25, 1), enable_events=True, key="-RES-"),
         sg.FolderBrowse(size=(11, 1)),],

        [sg.HorizontalSeparator()],

        [sg.Text(' '*10)],

        [sg.T(' '*5), sg.T('  Accessibility cutoff', justification='center'),
        sg.T(' '*2), sg.T('  Conservation cutoff', justification='center')],

        [sg.T(' '*13),
        sg.Slider(range=(0, 100), orientation='v', size=(8, 9), default_value=70, key='slider1'),
        sg.T(' '*18),
        sg.Slider(range=(0.0,1.0), orientation='v', resolution=.01, size=(8, 9), default_value=0.6, key='slider2')],

        [sg.HorizontalSeparator()],

        [sg.Text('\n')],
        [sg.Text('Click to add a protein name'), sg.B('+', key='-ADDPROT-')],
        [sg.Frame('', [[sg.T('Protein and chains')]], key='-COL1-')],

        [sg.HorizontalSeparator()],

        [sg.T('\n\n\n\n\n'),sg.T(' '*25), sg.Button('Submit id', size=(13, 1), key='-Submit id-', use_ttk_buttons=True),
         sg.Button('Submit folder', size=(13, 1), key='-Submit files-', use_ttk_buttons=True),],

    ]

    tab2 = [

        [sg.Text("PisaPy is a Python Wrapper for PDBePISA")],
        #[sg.Output(size=(60,30), key='-OUTPUT-')],
        #[sg.Button('Clear', use_ttk_buttons=True), sg.Button('Exit', use_ttk_buttons=True)]

    ]

    tab3 = [

        [sg.Text("Empty for the moment")],
        [sg.Button("", size=(1, 1), button_color=('#1f77b4', '#1f77b4'), key='Color')],

    ]

    layout = [[sg.TabGroup([[sg.Tab('PisaPy Params', tab1), sg.Tab('Shell', tab2), sg.Tab('Results', tab3)]])]] 

    return sg.Window("PisaPy", layout, ttk_theme=ttk_style)


def running():
    """
    """
    window = create_layouts()
    chooser = window['Color']
    color = None
    i = 0

    while True:
        event, values = window.read()
        #print(event, values)
        #print('-'*60)

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(".pdb")]
            window["-FILE LIST-"].update(fnames)

        if event == '-Submit id-':
            if (values['-PDB ID-'] == '') | (values['-PDB ID-'] == 'Please enter a pdb ID'):
                window.FindElement('-PDB ID-').Update('Please enter a pdb ID', text_color='red')
            else :
                rppy.run_pisa(0, values['-PDB ID-'])
                rppy.parse_files(0)
                #print(values['-PDB ID-'])
                #print(values['slider1'])
                #print(values['slider2'])

        if event == '-Submit files-':
            #rppy.run_pisa(1, values['-FOLDER-']+'/')
            dico = {}
            for k in values:
                if type(k) == str:
                    if '-PC' in k:
                        dico[values[k].split()[0]] = values[k].split()[1]

            rppy.parse_files(1, dico)
            print(values['-FOLDER-'])
            #print(values['slider1'])
            #print(values['slider2'])

        if event == 'Clear':
            window['-OUTPUT-'].update('')

        if event == 'Color':
            colors = tk.colorchooser.askcolor(
                    parent=chooser.ParentForm.TKroot, color=color)
            color = colors[1]
            chooser.Update(button_color=(color, color))

        if event == '-ADDPROT-':
            window.extend_layout(window['-COL1-'], [[sg.T('Protein chains'), sg.I(key=f'-PC-{i}-')]])
            i += 1

    window.close()


if __name__ == '__main__':
    running()