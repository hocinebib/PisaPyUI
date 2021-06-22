#!/usr/bin/python3
"""
Main code of the pipeline to get the residues conservation scores of a protein
from a protein name

  How to use
  ----------
First you need to have the python packages selenium, 

Then you can run the script with the following command :

    python Conservation.py "MexA MexB OprM"

  Author
  ------
    Hocine Meraouna

"""

import argparse
import os
import Auto_Uniprot as au
import Blast_Align as ba
import Auto_Mafft as am
import Res_Conserv_Score as rcs
import pandas as pd
from selenium import webdriver


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("protein_names", help="list of protein names", type=str)

    ARGS = PARSER.parse_args()

    PROT_NAMES = ARGS.protein_names

    browser = au.start()

    for p in PROT_NAMES.split():

        print(' --------------------------------------')
        print('|                Step I                |')
        print('|               --------               |')
        print('|              Uniprot id              |')
        print(' --------------------------------------')
        
        PID = au.uniprot_id(browser, p)

        print('Done :'+PID)

        print(' --------------------------------------')
        print('|               Step II                |')
        print('|              ---------               |')
        print('|                Blasp                 |')
        print(' --------------------------------------')

        ba.run_blastp(ba.get_fasta(PID)[0].seq, PID)

        FASTA = os.getcwd()+'/Results/'+PID+'_HomolSeq.fasta'

        print(' --------------------------------------')
        print('|              Step III                |')
        print('|             ----------               |')
        print('|                MAFFT                 |')
        print(' --------------------------------------')

        am.download_alignment(am.submit_query(am.start(), FASTA), FASTA)

        print(' --------------------------------------')
        print('|               Step IV                |')
        print('|              ---------               |')
        print('|      Residues Conservation Score     |')
        print(' --------------------------------------')

        MUL_ALI_FILE = os.getcwd()+'/Results/'+PID+'_HomolSeq_MAFFT.fasta'

        CONS_DICT = rcs.score_csv(rcs.launch_score_calculation(rcs.start(), MUL_ALI_FILE, p))

        pd.DataFrame.from_dict(CONS_DICT).to_csv(os.getcwd()+'/Results/'+p+'_ResConsScores.csv')

    browser.quit()
