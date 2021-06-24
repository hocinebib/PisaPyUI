#!/usr/bin/python3
"""
3d protein plot

  How to use
  ----------
First you need to have the python packages 

Then you can run the script with the following command :

    python 

  Author
  ------
    Hocine Meraouna

"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import glob
from Bio.PDB.Polypeptide import one_to_three
import os
from matplotlib.pyplot import cm


def remove_atom(x):
    """
    """
    return ' '.join(x.split('[')[0].split())


def change_tothree(x):
    """
    """
    return one_to_three(x.split()[0])+' '+x.split()[1]


def give_prot(chain, dicoo):
    """
    """
    for k in dicoo:
        if chain in dicoo[k]:
            return k
    return ''


def read_tables(path, proteins, dicoo, typee, acc_cutoff, cons_cutoff, color):
    """
    """

    dico = {'prot': [],'chain': [], 'res': [], 'x': [], 'y': [], 'z': []}

    target = [file for file in glob.glob(path+'/*') if (file.endswith('.pdb'))]

    with open(target[0], 'r') as pdb_file:
        for line in pdb_file:
            if line.startswith('ATOM'):
                if line.split()[2] == 'CA':
                    if len(line.split()[4]) == 1:
                        dico['res'].append(line.split()[3]+' '+line.split()[5])
                        dico['chain'].append(line.split()[4])
                        dico['prot'].append(give_prot(line.split()[4], dicoo))
                        dico['x'].append(float(line.split()[6]))
                        dico['y'].append(float(line.split()[7]))
                        dico['z'].append(float(line.split()[8]))
                    else:
                        dico['res'].append(line.split()[3]+' '+line.split()[4][1:])
                        dico['chain'].append(line.split()[4][0])
                        dico['prot'].append(give_prot(line.split()[4][0], dicoo))
                        dico['x'].append(float(line.split()[5]))
                        dico['y'].append(float(line.split()[6]))
                        dico['z'].append(float(line.split()[7]))


    df = pd.DataFrame.from_dict(dico)
    df = df.loc[(df['prot'].isin(proteins.split()))]
    df = df.reset_index()


    df2 = pd.read_csv(path+'/'+target[0].split('/')[-1].split('.')[0]+'_InteractionSheet.csv', usecols = [2,3,6,7])
    df2['res1'] = df2['res1'].apply(remove_atom)
    df2['res2'] = df2['res2'].apply(remove_atom)


    df3 = pd.DataFrame()

    for file in glob.glob(path+'/*'):
        if 'ResConsScores.csv' in file:
            if file.split('/')[-1].split('_')[0] in proteins:
                if df3.empty:
                    df3 = pd.read_csv(file, usecols = [1,2])
                    df3['prot'] = ((file.split('/')[-1].split('_')[0]+' ')*df3.shape[0]).split()
                else:
                    df3b = pd.read_csv(file, usecols = [1,2])
                    df3b['prot'] = ((file.split('/')[-1].split('_')[0]+' ')*df3b.shape[0]).split()
                    df3 = pd.concat([df3,df3b])

    df3['res'] = df3['res'].apply(change_tothree)


    df4 = pd.DataFrame()

    for file in glob.glob(path+'/*'):
        if ('chain_' in file) & (os.path.isdir(file)):
            if df4.empty:
                df4 = pd.read_csv(file+'/'+file.split('_')[-1]+'_access.csv', usecols=[1,2,3,4])
            else:
                df4b = pd.read_csv(file+'/'+file.split('_')[-1]+'_access.csv', usecols=[1,2,3,4])
                df4 = pd.concat([df4,df4b])

    acc_solo1 = list(df4['solo access'])
    acc_comp1 = list(df4['complex access'])

    acc1 = []

    for n, a in enumerate(acc_solo1):
        if ((abs(acc_solo1[n]-acc_comp1[n])) != 0):
            acc1.append((abs(acc_solo1[n]-acc_comp1[n])*100/(acc_solo1[n]+acc_comp1[n])))
        else:
            acc1.append(0.0)

    df4['acc_pourcentage'] = acc1

    return prepare_table(df, df2, df3, df4, acc_cutoff, cons_cutoff, proteins, typee, dicoo, color)



def prepare_table(df, df2, df3, df4, acc_cutoff, cons_cutoff, proteins, typee, dicoo, color):
    """
    """
    lst1 = []
    lst2 = []
    lst3 = []

    for r in df.iterrows():
        if not df2.loc[(df2['res1'] == r[1]['res']) & (df2['chain1'] == r[1]['chain'])].empty:
            lst1.append(1)
        elif not df2.loc[(df2['res2'] == r[1]['res']) & (df2['chain2'] == r[1]['chain'])].empty:
            lst1.append(1)
        else:
            lst1.append(0)
        if not df3.loc[(df3['res'] == r[1]['res']) & (df3['prot'] == give_prot(r[1]['chain'], dicoo))].empty:
            if float(df3.loc[(df3['res'] == r[1]['res']) & (df3['prot'] == give_prot(r[1]['chain'], dicoo))]['conservation score']) > 0.8:
                lst2.append(1)
            else:
                lst2.append(0)
        else:
            lst2.append(0)
    
    
        if float(df4.loc[(df4['res'] == r[1]['res']) & (df4['chain'] == r[1]['chain'])]['acc_pourcentage']) > acc_cutoff:
            lst3.append(1)
        elif float(df4.loc[(df4['res'] == r[1]['res']) & (df4['chain'] == r[1]['chain'])]['solo access']) != 0:
            if (df4['solo access'].max()/float(df4.loc[(df4['res'] == r[1]['res']) & (df4['chain'] == r[1]['chain'])]['solo access'])) < 1.6:
                if float(df4.loc[(df4['res'] == r[1]['res']) & (df4['chain'] == r[1]['chain'])]['acc_pourcentage']) > acc_cutoff/3:
                    lst3.append(1)
                else:
                     lst3.append(0)
            else:
                lst3.append(0)
        else:
            lst3.append(0)

    df['interaction'] = lst1
    df['conservation'] = lst2
    df['accessibility'] = lst3


    if typee == 1:
        dfs = df.loc[(df['conservation'] == 1)]
        dfs = dfs.reset_index()
    elif typee == 2:
        dfs = df.loc[(df['accessibility'] == 1)]
        dfs = dfs.reset_index()
    elif typee == 3:
        dfs = df.loc[(df['interaction'] == 1)]
        dfs = dfs.reset_index()
    else:
        dfs = df.loc[(df['conservation'] == 1) & (df['interaction'] == 1) & (df['accessibility'] == 1)]
        dfs = dfs.reset_index()
    
    return draw_plot(df, dfs, color)


def draw_plot(df, dfs, color):
    """
    """
    fig = plt.figure(figsize=(4,4))
    fig.patch.set_facecolor('grey')
    ax = fig.add_subplot(projection='3d')
    ax.set_facecolor('grey')
    names = np.array(dfs['chain']+' '+dfs['res'])


    colors = [cm.rainbow(i) for i in np.linspace(0, 0.9, len(df['chain'].unique()))]

    sc = ax.scatter(dfs['x'].values, dfs['y'].values, dfs['z'].values, color = color, s=20, depthshade = False, alpha = 0.7, picker = True)


    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="-|>"))

    annot.set_visible(False)


    for i, (grp_name, grp_idx) in enumerate(df.groupby('chain').groups.items()):
        y = df.iloc[grp_idx,4]
        x = df.iloc[grp_idx,5]
        z = df.iloc[grp_idx,6]
        ax.plot(x,y,z, label = grp_name, color = colors[i])

    ax.legend()

    def update_annot(ind):

        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos

        text = ""
        if (len(ind["ind"]) > 1):
            for n in ind["ind"] :
                text = text+" "+"['"+names[n]+"']\n"
        else :
            text = names[ind["ind"]]

        annot.set_text(text)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.axis('off')
    #plt.show()

    return fig

if __name__ == '__main__':
	import Prepare_plot
	print(help(Prepare_plot))