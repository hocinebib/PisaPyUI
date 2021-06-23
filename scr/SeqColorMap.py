#!/usr/bin/python3
"""
Code to plot colored maps of each of the protein chains, the color is based on the caracteristics extracted
previously like interaction, conservation or accessibility.

  How to use
  ----------
First you need to have the python packages PyQt5, seaborn, matplotlib, numpy, pandas and argparse, but you also need to
have the conservation csv file given by Res_Conserv_Score.py, the InteractionSheet.csv for the specific chain
given by Pisa_xml_parser.py and the rsa files given by NACCESS of the chain solo and in interaction.

Then you can run the script with the following command :
    python Sequence_color_map_New.py conserv_file interaction_file solo_rsa complex_rsa chain --cutoff1 60 --cutoff2 0.6

Exemple :
    python Sequence_color_map.py MexBCO_2.csv InteractionSheet2.csv MexB_J_solo.rsa MexB_Jcomplex.rsa J --cutoff1 60 --cutoff2 0.6

  Author
  ------
    Hocine Meraouna
"""


import pandas as pd
import os
from os import listdir
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from glob import glob
from os.path import isfile, join


def keep_res_nbr1(x):
    return x.split('[')[0].split()[1]


def keep_res_nbr2(x):
    return x.split()[1]


def colormap_sequence(conserv_df, conserv_cutoff, interaction_df, access_solo_df, access_trio_df, diff_access, chain, prot, inter_chains, fstcm, sndcm, path):
    """
    """

    fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6,1, figsize= (170,6))
    st = fig.suptitle(prot+" chain "+chain+" informations", fontsize=30)
 
    sns.heatmap(conserv_df, vmin = float(conserv_df.min(axis=1)[0]), vmax = float(conserv_df.max(axis=1)[0]), 
        cmap=fstcm, linewidth = 0.5, ax=ax1)

    sns.heatmap(conserv_cutoff, vmin = conserv_cutoff.min(axis=1)[0], vmax = conserv_cutoff.max(axis=1)[0], 
        cmap=fstcm, linewidth = 0.5, ax=ax2)

    sns.heatmap(interaction_df, vmin = interaction_df.min(axis=1)[0], vmax = interaction_df.max(axis=1)[0], 
        cmap='Set2', linewidth = 0.5, ax=ax3, cbar_kws={"ticks":list(range(0,len(inter_chains)+1)), "label": ' '.join(inter_chains)})

    sns.heatmap(access_solo_df, vmin = access_solo_df.min(axis=1)[0], vmax = access_solo_df.max(axis=1)[0], 
        cmap=sndcm, linewidth = 0.5, ax=ax4)

    sns.heatmap(access_trio_df, vmin = access_trio_df.min(axis=1)[0], vmax = access_trio_df.max(axis=1)[0], 
        cmap=sndcm, linewidth = 0.5, ax=ax5)

    sns.heatmap(diff_access, vmin = diff_access.min(axis=1)[0], vmax = diff_access.max(axis=1)[0], 
        cmap=sndcm, linewidth = 0.5, ax=ax6)
    
    ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, fontsize=8)
    ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0, fontsize=8)
    ax3.set_yticklabels(ax3.get_yticklabels(), rotation=0, fontsize=8)
    ax4.set_yticklabels(ax4.get_yticklabels(), rotation=0, fontsize=8)
    ax5.set_yticklabels(ax5.get_yticklabels(), rotation=0, fontsize=8)
    ax6.set_yticklabels(ax6.get_yticklabels(), rotation=0, fontsize=8)

    ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)
    ax2.set_xticklabels(ax2.get_xticklabels(), visible=False)
    ax3.set_xticklabels(ax3.get_xticklabels(), visible=False)
    ax4.set_xticklabels(ax4.get_xticklabels(), visible=False)
    ax5.set_xticklabels(ax5.get_xticklabels(), visible=False)

    plt.savefig(path+chain+'_ColorMap.png')

def cutoff_tables(res_path, cons_cutoff, acc_cutoff, chain, col1, col2):
    """
    """
    for file in glob(res_path+'*'):
        if '_InteractionSheet.csv' in file:
            df1 = pd.read_csv(file, usecols = [2,3,6,7])
            df1['res1'] = df1['res1'].apply(keep_res_nbr1)
            df1['res2'] = df1['res2'].apply(keep_res_nbr1)
            df1 = df1.loc[(df1['chain1'] == chain) | (df1['chain2'] == chain)]
    
    df2 = pd.read_csv(res_path+'chain_'+chain+'/'+chain+'_access.csv', usecols = [1,2,3,4])
    df2['res'] = df2['res'].apply(keep_res_nbr2)
    acc_solo1 = list(df2['solo access'])
    acc_comp1 = list(df2['complex access'])

    acc1 = []

    for n, a in enumerate(acc_solo1):
        if ((abs(acc_solo1[n]-acc_comp1[n])) != 0):
            acc1.append((abs(acc_solo1[n]-acc_comp1[n])*100/(acc_solo1[n]+acc_comp1[n])))
        else:
            acc1.append(0.0)

    df2['acc_pourcentage'] = acc1

    
    for file in glob(res_path+'*'):
        if '_ResConsScores.csv' in file:
            df3 = pd.read_csv(file,usecols=[1,2])
            df3['res'] = df3['res'].apply(keep_res_nbr2)

    dico = {'resnbr': [], 'interaction': [], 'conservation': [],
        'access_solo': [], 'access_complex': [], 'access_cutoff': [],
        'conserv_cutoff': []}
    dico['resnbr'] = list(df2['res'])


    for r in df3.iterrows():
        if (int(r[1]['res']) <= int(list(df2['res'])[-1])):
            dico['conservation'].append(r[1]['conservation score'])
            if r[1]['conservation score'] > cons_cutoff:
                dico['conserv_cutoff'].append(1)
            else:
                dico['conserv_cutoff'].append(0)
            if not df1.loc[df1['res1'] == r[1]['res']].empty:
                dico['interaction'].append(list(df1['chain2'].unique()).index(list(df1.loc[df1['res1'] == r[1]['res']]['chain2'])[0])+1)
            else:
                dico['interaction'].append(0)
            dico['access_solo'].append(float(df2.loc[(df2['res'] == r[1]['res'])]['solo access']))
            dico['access_complex'].append(float(df2.loc[(df2['res'] == r[1]['res'])]['complex access']))
            if float(df2.loc[(df2['res'] == r[1]['res'])]['acc_pourcentage']) > acc_cutoff:
                dico['access_cutoff'].append(1)
            elif float(df2.loc[(df2['res'] == r[1]['res'])]['solo access']) != 0:
                if (df2['solo access'].max()/float(df2.loc[(df2['res'] == r[1]['res'])]['solo access'])) < 1.6:
                    if float(df2.loc[(df2['res'] == r[1]['res'])]['acc_pourcentage']) > acc_cutoff/3:
                        dico['access_cutoff'].append(1)
                    else:
                        dico['access_cutoff'].append(0)
                else:
                    dico['access_cutoff'].append(0)
            else:
                dico['access_cutoff'].append(0)


    df5 = pd.DataFrame.from_dict(dico)
    df5 = df5.set_index('resnbr')
    df5_transposed = df5.T


    conserv_df = df5_transposed.iloc[[1]]
    conserv_cutoff = df5_transposed.iloc[[5]]
    interaction_df1 = df5_transposed.iloc[[0]]
    access_solo_df = df5_transposed.iloc[[2]]
    access_trio_df = df5_transposed.iloc[[3]]
    diff_access = df5_transposed.iloc[[4]]
    prot = res_path.split('/')[-2].split('_')[0]
    inter_chains = list(df1['chain2'].unique())

    colors = ['white', col1]
    cm = LinearSegmentedColormap.from_list("Custom", colors, N=100)
    colors2 = ['white', col2]
    cm2 = LinearSegmentedColormap.from_list("Custom", colors2, N=100)

    colormap_sequence(conserv_df, conserv_cutoff, interaction_df1, access_solo_df, access_trio_df,
        diff_access, chain, prot, inter_chains, cm, cm2, res_path)


if __name__ == '__main__':
    import SeqColorMap
    print(help(SeqColorMap))