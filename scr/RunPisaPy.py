#!/usr/bin/python3
"""
Code to 

  How to use
  ----------
First you need to have the python packages 

Then you can run the script with the following command :

 with pd ids:
    python RunPisaPy.py "6ta5 6iol" /home/meraouna/Téléchargements/naccess2.1.1/naccess Data/MexAB-OprM.txt

 with pd files:
    python RunPisaPy.py Data/ --d 1 /home/meraouna/Téléchargements/naccess2.1.1/naccess Data/MexAB-OprM.txt

  Author
  ------
    Hocine Meraouna

"""

import argparse
import os
import sys
import PisaAuto_id as pai
import PisaAuto_file as paf
import Pisa_xml_parser as pxp
import Parse_Interfacetable as pi
import Auto_Uniprot as au
import Blast_Align as ba
import Auto_Mafft as am
import Res_Conserv_Score as rcs
import pandas as pd
import Auto_Naccess as an
import Download_pdbfasta as dpf
import json
from os import listdir
from os.path import isfile
from glob import glob
from selenium import webdriver
from Bio.PDB.Polypeptide import three_to_one


def get_dict(dico_file):
    """
    """
    with open(dico_file, 'r') as file:
        dicoprot = file.read()

    res = json.loads(dicoprot)

    return res


def run_pisa(TYPE, PDB_ID, RES_PATH):
    """
    """
    print(' '*60)

    if TYPE == 0:
        for protein in PDB_ID.split():
            pai.download_xmls(pai.launch_pdb_id(pai.start(), protein), protein, RES_PATH)

    elif TYPE == 1:
        PDB_FILES = sorted([PDB_ID+f for f in listdir(PDB_ID) 
            if ((isfile(PDB_ID+f)) and 
                (f.split(".")[-1] == "pdb"))], key=str.lower)

        for i, file in enumerate(PDB_FILES):
            print("## pdb file "+str(i+1)+"/"+str(len(PDB_FILES)))
            driver = pai.start()
            pai.download_xmls(paf.launch_pdb_file(driver, file), file.split('/')[-1], RES_PATH)
            driver.quit()


def parse_files(TYPE, DICO_CHAINS, RES_PATH):
    """
    """
    print("5- Converting xml files to csv :")

    for direct in glob(RES_PATH+'*/'):
        if 'xml_files' in direct:

            if TYPE == 0:
                current_pdb = direct.split('xml_files')[1].split('.')[0][:-1]
                if not os.path.exists(RES_PATH+current_pdb+'.pdb/'):
                    os.makedirs(RES_PATH+current_pdb+'.pdb/')
                pxp.create_df(pxp.interfacetable_parse(RES_PATH+'xml_files'+\
                    current_pdb+'/interfacetable.xml'), DICO_CHAINS).to_csv(RES_PATH+current_pdb+'.pdb/'+current_pdb+"_InteractionSheet.csv")
                pd.DataFrame.from_dict(pi.parse_interface(RES_PATH+'xml_files'+\
                    current_pdb+'/interfacetable.xml')).to_csv(RES_PATH+current_pdb+'.pdb/'+current_pdb+"_InterfaceTable.csv")

            elif TYPE == 1:
                current_pdb = direct.split('xml_files')[1][:-1]
                if not os.path.exists(RES_PATH+current_pdb):
                    os.makedirs(RES_PATH+current_pdb)
                pxp.create_df(pxp.interfacetable_parse(RES_PATH+'xml_files'+\
                    current_pdb+'/interfacetable.xml'), DICO_CHAINS).to_csv(RES_PATH+current_pdb+'/'+current_pdb+"_InteractionSheet.csv")
                pd.DataFrame.from_dict(pi.parse_interface(RES_PATH+'xml_files'+\
                    current_pdb+'/interfacetable.xml')).to_csv(RES_PATH+current_pdb+'/'+current_pdb+"_InterfaceTable.csv")

    print("Done.")


def run_naccess(TYPE, PDB_ID, NACCESS_PATH, RES_PATH):
    """
    """
    if TYPE == 1:
        for file in glob(PDB_ID+'*.pdb'):

            dic = an.interacting_chains(RES_PATH+file.split('/')[-1]+'/'+file.split('/')[-1]+"_InteractionSheet.csv")

            print("1)- Generating Solo chains files :")

            an.pdb_solo_chains(PDB_ID+file.split('/')[-1])

            print("Done.")

            print("2)- Generating chains with interacting partners files :")
            
            an.pdb_complex_chains(PDB_ID+file.split('/')[-1], dic)

            print('Done.')

            print("3)- Generating accessibility csv files :")

            an.call_naccess(dic, NACCESS_PATH, file.split('/')[-1])  

            print('Done.')

    elif TYPE == 0:
        print('- Downloading pdb files and calculating accessibility :')

        for protein in PDB_ID.split():
            print(protein)

            dpf.download_pdb(protein, RES_PATH)

            dic = an.interacting_chains(RES_PATH+protein+'.pdb/'+protein+"_InteractionSheet.csv")

            print("1)- Generating Solo chains files :")

            an.pdb_solo_chains(RES_PATH+protein+'.pdb/'+protein+'.pdb')

            print("Done.")

            print("2)- Generating chains with interacting partners files :")
            
            an.pdb_complex_chains(RES_PATH+protein+'.pdb/'+protein+'.pdb', dic)

            print('Done.')

            print("3)- Generating accessibility csv files :")

            an.call_naccess(dic, NACCESS_PATH, protein+'.pdb')  

            print('Done.')


def run_res_conserv(TYPE, PDB_ID, DICO_CHAINS, RES_PATH):
    """
    """
    if TYPE == 0:
        for protein in PDB_ID.split():
            for p in DICO_CHAINS:
                print("1)- Finding uniprot ids of  :", p)
                browser = au.start()
                PID = au.uniprot_id(browser, p)
                browser.quit()
                print('Done.')
            
                print("2)- Finding homologous sequences with blastp on :", p)
                ba.run_blastp(ba.get_fasta(PID)[0].seq, PID, RES_PATH+protein+'.pdb/')
                FASTA = RES_PATH+protein+'.pdb/'+PID+'_HomolSeq.fasta'
                print('Done.')

                print("3)- MAFFT Multiple sequence alignment for :", p)
                am.download_alignment(am.submit_query(am.start(RES_PATH), FASTA), FASTA, RES_PATH)
                print('Done.')

                print("4)- Calculating residus conservation scores for :", p)
                MUL_ALI_FILE = RES_PATH+protein+'.pdb/'+PID+'_HomolSeq_MAFFT.fasta'
                CONS_DICT = rcs.score_csv(rcs.launch_score_calculation(rcs.start(), MUL_ALI_FILE, p, RES_PATH))
                pd.DataFrame.from_dict(CONS_DICT).to_csv(RES_PATH+protein+'.pdb/'+p+'_ResConsScores.csv')
                print('Done.')

    elif TYPE == 1:
        for file in glob(PDB_ID+'*.pdb'):
            for k in DICO_CHAINS:
                print(k)
                seq = ''
                lst = []
                with open(file, 'r') as pdb_file:
                    for line in pdb_file:
                        if line.startswith('ATOM'):
                            if line.split()[4][0] == DICO_CHAINS[k][0]:
                                if len(line.split()[4]) == 1:
                                    if line.split()[5] not in lst:
                                        lst.append(line.split()[5])
                                        seq += three_to_one(line.split()[3])
                                elif len(line.split()[4]) > 1:
                                    if line.split()[4][1:] not in lst:
                                        lst.append(line.split()[4][1:])
                                        seq += three_to_one(line.split()[3])

                if len(seq) > 2:
                    print("1)- Finding homologous sequences with blastp on :", k)
                    idd = file.split('/')[-1]+'/'+k+'_'+file.split('/')[-1].split('.')[0]
                    ba.run_blastp(seq, idd, RES_PATH)
                    FASTA = RES_PATH+idd+'_HomolSeq.fasta'
                    print('Done.')

                    print("2)- MAFFT Multiple sequence alignment for :", k)
                    am.download_alignment(am.submit_query(am.start(RES_PATH), FASTA), FASTA, RES_PATH)
                    print('Done.')

                    print("3)- Calculating residus conservation scores for :", k)
                    MUL_ALI_FILE = RES_PATH+idd+'_HomolSeq_MAFFT.fasta'
                    CONS_DICT = rcs.score_csv(rcs.launch_score_calculation(rcs.start(), MUL_ALI_FILE, k, RES_PATH))
                    df = pd.DataFrame.from_dict(CONS_DICT)
                    for i, r in enumerate(df.iterrows()):
                        lst[i] = r[1]['res'].split()[0]+' '+lst[i]
                    df['res'] = lst
                    df.to_csv(RES_PATH+idd+'_ResConsScores.csv')
                    print('Done.')



if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("pdb_id", help="pdb ids separated by spaces or path to a directory with pdb files", type=str)

    PARSER.add_argument("--d", help="0 if it's a pdb id and 1 if it's path to pdb files", default=0, type=int)

    PARSER.add_argument("nacc_path", help="the full path to the naccess bin", type=str)

    PARSER.add_argument("prot_dict", help="a file containing the chains of each protein", type=str)

    ARGS = PARSER.parse_args()

    PDB_ID = ARGS.pdb_id

    TYPE = ARGS.d

    NACCESS_PATH = ARGS.nacc_path

    DICO_CHAINS = get_dict(ARGS.prot_dict)

    print(' '*20+'+'+'-'*38+'+')
    print(' '*20+'|              Step III                |')
    print('='*20+'|             ----------               |'+'='*20)
    print(' '*20+'|        Align & Conservation          |')
    print(' '*20+'+'+'-'*38+'+')
    print('\n'+'-'*80)


    if TYPE == 0:
        for protein in PDB_ID.split():
            for p in DICO_CHAINS:
                print("1)- Finding uniprot ids of  :", p)
                browser = au.start()
                PID = au.uniprot_id(browser, p)
                browser.quit()
                print('Done.')
            
                print("2)- Finding homologous sequences with blastp on :", p)
                ba.run_blastp(ba.get_fasta(PID)[0].seq, PID)
                FASTA = os.getcwd()+'/Results/'+protein+'.pdb/'+PID+'_HomolSeq.fasta'
                print('Done.')

                print("3)- MAFFT Multiple sequence alignment for :", p)
                am.download_alignment(am.submit_query(am.start(), FASTA), FASTA)
                print('Done.')

                print("4)- Calculating residus conservation scores for :", p)
                MUL_ALI_FILE = os.getcwd()+'/Results/'+protein+'.pdb/'+PID+'_HomolSeq_MAFFT.fasta'
                CONS_DICT = rcs.score_csv(rcs.launch_score_calculation(rcs.start(), MUL_ALI_FILE, p))
                pd.DataFrame.from_dict(CONS_DICT).to_csv(os.getcwd()+'/Results/'+protein+'.pdb/'+p+'_ResConsScores.csv')
                print('Done.')

    elif TYPE == 1:
        for file in glob(PDB_ID+'*.pdb'):
            for k in DICO_CHAINS:
                seq = ''
                lst = []
                with open(file, 'r') as pdb_file:
                    for line in pdb_file:
                        if line.startswith('ATOM'):
                            if line.split()[4][0] == DICO_CHAINS[k][0]:
                                if len(line.split()[4]) == 1:
                                    if line.split()[5] not in lst:
                                        lst.append(line.split()[5])
                                        seq += three_to_one(line.split()[3])
                                elif len(line.split()[4]) > 1:
                                    if line.split()[4][1:] not in lst:
                                        lst.append(line.split()[5])
                                        seq += three_to_one(line.split()[3])

                if len(seq) > 2:
                    print("1)- Finding homologous sequences with blastp on :", k)
                    idd = file.split('/')[-1]+'/'+k+'_'+file.split('/')[-1].split('.')[0]
                    ba.run_blastp(seq, idd)
                    FASTA = os.getcwd()+'/Results/'+idd+'_HomolSeq.fasta'
                    print('Done.')

                    print("2)- MAFFT Multiple sequence alignment for :", k)
                    am.download_alignment(am.submit_query(am.start(), FASTA), FASTA)
                    print('Done.')

                    print("3)- Calculating residus conservation scores for :", k)
                    MUL_ALI_FILE = os.getcwd()+'/Results/'+idd+'_HomolSeq_MAFFT.fasta'
                    CONS_DICT = rcs.score_csv(rcs.launch_score_calculation(rcs.start(), MUL_ALI_FILE, p))
                    pd.DataFrame.from_dict(CONS_DICT).to_csv(os.getcwd()+'/Results/'+idd+'_ResConsScores.csv')
                    print('Done.')


"""


    print(' '*20+'+'+'-'*38+'+')
    print(' '*20+'|                Step I                |')
    print('='*20+'|               --------               |'+'='*20)
    print(' '*20+'|               PDBePISA               |')
    print(' '*20+'+'+'-'*38+'+')
    print('\n'+'-'*80)

    if TYPE == 0:
        for protein in PDB_ID.split():
            pai.download_xmls(pai.launch_pdb_id(pai.start(), protein), protein)

    elif TYPE == 1:
        PDB_FILES = sorted([PDB_ID+f for f in listdir(PDB_ID) 
            if ((isfile(PDB_ID+f)) and 
                (f.split(".")[-1] == "pdb"))], key=str.lower)

        for i, file in enumerate(PDB_FILES):
            print("## pdb file "+str(i+1)+"/"+str(len(PDB_FILES)))
            driver = pai.start()
            pai.download_xmls(paf.launch_pdb_file(driver, file), file.split('/')[-1])
            driver.quit()

    else:
           sys.exit("main.py: error: --d should be 1 (for directory) or 0 (for id) nothing else.")

    print("5- Converting xml files to csv :")

    for direct in glob('Results/*/'):
        if 'xml_files' in direct:

            if TYPE == 0:
                current_pdb = direct.split('xml_files')[1].split('.')[0][:-1]
                if not os.path.exists('Results/'+current_pdb+'.pdb/'):
                    os.makedirs('Results/'+current_pdb+'.pdb/')
                pxp.create_df(pxp.interfacetable_parse('Results/xml_files'+\
                    current_pdb+'/interfacetable.xml'), DICO_CHAINS).to_csv("Results/"+current_pdb+'.pdb/'+current_pdb+"_InteractionSheet.csv")
                pd.DataFrame.from_dict(pi.parse_interface('Results/xml_files'+\
                    current_pdb+'/interfacetable.xml')).to_csv("Results/"+current_pdb+'.pdb/'+current_pdb+"_InterfaceTable.csv")

            elif TYPE == 1:
                current_pdb = direct.split('xml_files')[1][:-1]
                if not os.path.exists('Results/'+current_pdb):
                    os.makedirs('Results/'+current_pdb)
                pxp.create_df(pxp.interfacetable_parse('Results/xml_files'+\
                    current_pdb+'/interfacetable.xml'), DICO_CHAINS).to_csv("Results/"+current_pdb+'/'+current_pdb+"_InteractionSheet.csv")
                pd.DataFrame.from_dict(pi.parse_interface('Results/xml_files'+\
                    current_pdb+'/interfacetable.xml')).to_csv("Results/"+current_pdb+'/'+current_pdb+"_InterfaceTable.csv")

    print("Done.")

    print(' '*20+'+'+'-'*38+'+')
    print(' '*20+'|               Step II                |')
    print('='*20+'|              ---------               |'+'='*20)
    print(' '*20+'|               NACCESS                |')
    print(' '*20+'+'+'-'*38+'+')
    print('\n'+'-'*80)

    if TYPE == 1:
        for file in glob(PDB_ID+'*.pdb'):

            dic = an.interacting_chains("Results/"+file.split('/')[-1]+'/'+file.split('/')[-1]+"_InteractionSheet.csv")

            print("1)- Generating Solo chains files :")

            an.pdb_solo_chains("Data/"+file.split('/')[-1])

            print("Done.")

            print("2)- Generating chains with interacting partners files :")
            
            an.pdb_complex_chains("Data/"+file.split('/')[-1], dic)

            print('Done.')

            print("3)- Generating accessibility csv files :")

            an.call_naccess(dic, NACCESS_PATH, file.split('/')[-1])  

            print('Done.')

    elif TYPE == 0:
        print('- Downloading pdb files and calculating accessibility :')

        for protein in PDB_ID.split():

            dpf.download_pdb(protein)

            dic = an.interacting_chains("Results/"+protein+'.pdb/'+protein+"_InteractionSheet.csv")

            print("1)- Generating Solo chains files :")

            an.pdb_solo_chains("Results/"+protein+'.pdb/'+protein+'.pdb')

            print("Done.")

            print("2)- Generating chains with interacting partners files :")
            
            an.pdb_complex_chains("Results/"+protein+'.pdb/'+protein+'.pdb', dic)

            print('Done.')

            print("3)- Generating accessibility csv files :")

            an.call_naccess(dic, NACCESS_PATH, protein+'.pdb')  

            print('Done.')

"""
