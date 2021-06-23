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
import numpy as np
import SeqColorMap as scm
import csv
import traceback
import plot as p
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def table_from_csv(filename):
    """
    Hirschdude
    https://stackoverflow.com/questions/58378205/cannot-build-table-with-pysimplegui
    """
    data = []
    header_list = []

    if filename is not None:
        with open(filename, "r") as infile:
            reader = csv.reader(infile)
            header_list = next(reader)
            data = list(reader)

    return data, header_list


def create_layouts():
    """
    """
    sg.theme('SystemDefaultForReal')
    ttk_style = 'alt'
    sg.change_look_and_feel('DarkBlue')

    tab1_left = [

        [sg.Text('You can either run PisaPy using pdb IDs or pdb files')],

        [sg.HorizontalSeparator()],

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

        [sg.Text('Click to add a protein name'), sg.B('+', key='-ADDPROT-')],
        [sg.Frame('', [[sg.T('Protein and chains')]], key='-COL1-')],

        [sg.HorizontalSeparator()],

        [sg.T('\n\n\n\n\n'),sg.T(' '*25), sg.Button('Submit id', size=(13, 1), key='-Submit id-', use_ttk_buttons=True),
         sg.Button('Submit folder', size=(13, 1), key='-Submit files-', use_ttk_buttons=True),],

    ]

    tab1_right = [

        [sg.Text("PisaPy is a Python Wrapper for PDBePISA")],
        [sg.Output(size=(50,45), key='-OUTPUT-')],
        [sg.Button('Clear', use_ttk_buttons=True), sg.Button('Exit', use_ttk_buttons=True)]

    ]

    tab1 = [

        [
         sg.Column(tab1_left),
         sg.VSeperator(),
         sg.Column(tab1_right),
        ]

    ]

    column = [[sg.Image(filename='other_files/empty_ColorMap.png', key="-IMAGE-")]]

    tab3 = [

        [sg.Text('Select the protein and the chain for witch the ColorMap will be generated')],

        [sg.HorizontalSeparator()],

        [sg.Text("\n"),
         sg.Text("Results directory"),
         sg.In(size=(25, 1), enable_events=True, key="-RESDIR-"),
         sg.FolderBrowse(size=(11, 1)),
         sg.Text(' '*10+'Chain'), sg.InputText(size=(25, 1), key="-CHAIN-"),],
        [sg.Button("", size=(1, 1), button_color=('#117e39', '#117e39'), key='Color'), sg.Text("high conservation color")],
        [sg.Button("", size=(1, 1), button_color=('#2006d9', '#2006d9'), key='Color2'), sg.Text("high accessibility color")],

        [sg.HorizontalSeparator()],

        [sg.Text(' '*10)],

        [sg.T(' '*5), sg.T('  Accessibility cutoff', justification='center'),
        sg.T(' '*2), sg.T('  Conservation cutoff', justification='center')],

        [sg.T(' '*13),
        sg.Slider(range=(0, 100), orientation='v', size=(8, 9), default_value=70, key='slider1'),
        sg.T(' '*18),
        sg.Slider(range=(0.0,1.0), orientation='v', resolution=.01, size=(8, 9), default_value=0.6, key='slider2'),
        sg.T(' '*30),
        sg.Button('Plot', size=(13, 1), key='-DRAW-', use_ttk_buttons=True),],

        [sg.HorizontalSeparator()],

        [sg.Column(column, size=(850,240), scrollable=True)]

    ]

    tab4 = [

        [
         sg.Column([

        [sg.Text("PDBePISA :")],
        [sg.Text("  - Krissinel E, Henrick K. Inference of macromolecular assemblies from\
 crystalline state. J Mol Biol. 2007 Sep\n21;372(3):774-97. doi: 10.1016/j.jmb.2007.05.022.\
 Epub 2007 May 13. PMID: 17681537.")],
        [sg.Text("  - E. Krissinel and K. Henrick (2005). Detection of Protein Assemblies in\
 Crystals. In: M.R.Berthold et.al.\n(Eds.): CompLife 2005, LNBI 3695, pp. 163--174.\
 Springer-Verlag Berlin Heidelberg.")],
        [sg.Text("- Krissinel E. Crystal contacts as nature's docking solutions. J Comput\
 Chem. 2010 Jan 15;31(1):133-43.\ndoi: 10.1002/jcc.21303. PMID: 19421996. \n")],

        [sg.Text("NACCESS :")],
        [sg.Text("  - S. Hubbard and J. Thornton. 1993. NACCESS, Computer Program. Department\
 of Biochemistry Molecular Biology,\nUniversity College London. \n")],

        [sg.Text("Blastp :")],
        [sg.Text("  - Altschul, S.F., Gish, W., Miller, W., Myers, E.W. & Lipman, D.J. (1990)\
 'Basic local alignment search tool.'\nJ. Mol. Biol. 215:403-410.")],
        [sg.Text("  - Gish, W. & States, D.J. (1993) 'Identification of protein coding regions\
 by database similarity search.'\nNature Genet. 3:266-272.")],
        [sg.Text("  - Altschul, S.F., Madden, T.L., Schäffer, A.A., Zhang, J., Zhang, Z., Miller,\
 W. & Lipman, D.J. (1997)\n'Gapped BLAST and PSI-BLAST: a new generation of protein database\
 search programs.' Nucleic Acids Res. 25:3389-3402.\n")],

        [sg.Text("MAFFT :")],
        [sg.Text("  - Katoh K, Rozewicki J, Yamada KD. MAFFT online service: multiple sequence\
 alignment, interactive sequence choice\nand visualization. Brief Bioinform. 2019 Jul 19;20(4):1160-1166.\
 doi: 10.1093/bib/bbx108. PMID: 28968734;\nPMCID: PMC6781576.")],
        [sg.Text("  - Katoh K, Misawa K, Kuma K, et al. . MAFFT: a novel method for rapid multiple\
 sequence alignment based on fast\nFourier transform. Nucleic Acids Res 2002;30:3059–66.")],
        [sg.Text("  - Katoh K, Standley DM.. MAFFT multiple sequence alignment software version 7:\
 improvements in performance and\nusability. Mol Biol Evol 2013;30(4):772–80.")],
        [sg.Text("  - Kuraku S, Zmasek CM, Nishimura O, Katoh K. aLeaves facilitates on-demand\
 exploration of metazoan gene family\ntrees on MAFFT sequence alignment server with enhanced\
 interactivity. Nucleic Acids Res. 2013 Jul;41(Web Server\nissue):W22-8. doi: 10.1093/nar/gkt389.\
 Epub 2013 May 15. PMID: 23677614; PMCID: PMC3692103.\n")],

        [sg.Text("Jensen-Shannon divergence Scoring :")],
        [sg.Text("  - Capra JA and Singh M. Predicting functionally important residues from sequence\
 conservation. Bioinformatics,\n23(15):1875-82, 2007.\n")],

        [sg.Text("PisaPY :")],
        [sg.Text("  - Made by Hocine Meraouna as part of an internship at the University of Reunion\
 supervised by Catherine Etchebest\nand Anne-Elisabeth Mozla\n")],

        [sg.Text(' '*110+'2021')],

    ], size = (850,560), scrollable=True)]

    ]

    data, header_list = table_from_csv('other_files/empty_csv.csv')

    tab5 = [

        [sg.Text("Select CSV file to display"), sg.Input(key='-CSVF-'), sg.FileBrowse('Choose',
            file_types=(("CSV Files","*.csv"),))],[sg.Button("Display", key='-DISTAB-', use_ttk_buttons=True),
         sg.Text(' '*16+'The file must correspond to the Interaction Sheet')],
        [sg.Table(values=data, headings=header_list,
            auto_size_columns=True, max_col_width=25, justification='middle', num_rows=45, key='-TABLE-')]

    ]

    tab6 = [

        [sg.Text("Select the result folder"),
         sg.In(size=(25, 1), enable_events=True, key="-STRCT-"),
         sg.FolderBrowse(size=(11, 1)),],
        [sg.Radio('Show high conservation', "RADIO1", default=False)],
        [sg.Radio('Show high accessibility', "RADIO1", default=False)],
        [sg.Radio('Show high cons & acc', "RADIO1", default=True)],
        [sg.Text('What proteins to show   '), sg.InputText(size=(25, 1), key="-PRTS-"),
        sg.Text(' '*50), sg.Button('Show Structure', size=(14, 1), key='-PLOT-', use_ttk_buttons=True)],
        [sg.HorizontalSeparator()],
        [sg.Canvas(key='-CANVAS-')]

    ]

    layout = [[sg.TabGroup([[sg.Tab('PisaPy Params', tab1), sg.Tab('SequenceColorMap', tab3),
        sg.Tab('Structure', tab6), sg.Tab('CSV', tab5), sg.Tab('Credit', tab4)]])]] 

    return sg.Window("PisaPy", layout, ttk_theme=ttk_style, finalize=True)


def running():
    """
    """
    window = create_layouts()
    chooser = window['Color']
    color = '#039136'
    chooser2 = window['Color2']
    color2 = '#0918d9'
    i = 0

    try:

        while True:
            event, values = window.read()
    
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
                    rppy.run_pisa(0, values['-PDB ID-'], values['-RES-']+'/')
                    dico = {}
                    for k in values:
                        for k in values:
                            if type(k) == str:
                                if '-PC' in k:
                                    dico[values[k].split()[0]] = values[k].split()[1]

                    rppy.parse_files(0, dico, values['-RES-']+'/')
                    rppy.run_naccess(0, values['-PDB ID-'], values['-FOLDER1-']+'/naccess', values['-RES-']+'/')
                    rppy.run_res_conserv(0, values['-PDB ID-'], dico, values['-RES-']+'/')

            if event == '-Submit files-':
                print('-'*60)
                rppy.run_pisa(1, values['-FOLDER-']+'/', values['-RES-']+'/')
                dico = {}
                for k in values:
                    for k in values:
                        if type(k) == str:
                            if '-PC' in k:
                                dico[values[k].split()[0]] = values[k].split()[1]

                rppy.parse_files(1, dico, values['-RES-']+'/')
                rppy.run_naccess(1, values['-FOLDER-']+'/', values['-FOLDER1-']+'/naccess', values['-RES-']+'/')
                rppy.run_res_conserv(1, values['-FOLDER-']+'/', dico, values['-RES-']+'/')
                print('-'*60)

            if event == 'Clear':
                window['-OUTPUT-'].update('')

            if event == 'Color':
                colors = tk.colorchooser.askcolor(
                        parent=chooser.ParentForm.TKroot, color=color)
                color = colors[1]
                chooser.Update(button_color=(color, color))

            if event == 'Color2':
                colors2 = tk.colorchooser.askcolor(
                        parent=chooser.ParentForm.TKroot, color=color2)
                color2 = colors2[1]
                chooser2.Update(button_color=(color2, color2))

            if event == '-ADDPROT-':
                window.extend_layout(window['-COL1-'], [[sg.T('Protein chains'), sg.I(key=f'-PC-{i}-')]])
                i += 1

            if event == '-DRAW-':
                if (values['-CHAIN-'] == '') | (values['-CHAIN-'] == 'Please enter a chain'):
                    window.FindElement('-CHAIN-').Update('Please enter a chain', text_color='red')
                else :
                    scm.cutoff_tables(values['-RESDIR-']+'/', values['slider2'], values['slider1'], values['-CHAIN-'],
                        color, color2)
                    window["-IMAGE-"].update(filename=values['-RESDIR-']+'/'+values['-CHAIN-']+'_ColorMap.png')

            if event == '-DISTAB-':
                if (values['-CSVF-'] == '') | (not values['-CSVF-'].endswith('.csv')):
                    window.FindElement('-CSVF-').Update('Please choose a csv file', text_color='red')
                else:
                    data, header_list = table_from_csv(values['-CSVF-'])
                    window['-TABLE-'].update(values=data)

            if event == '-PLOT-':
                fig = p.the_plot()
                fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

        window.close()
    except Exception as e:
        tb = traceback.format_exc()
        sg.Print(f'An error happened.  Here is the info:', e, tb)
        sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)


if __name__ == '__main__':
    running()