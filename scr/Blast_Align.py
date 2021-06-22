#!/usr/bin/python3
"""
Code to get the homologous sequences of a given protein using blastp

  How to use
  ----------
First you need to have the python packages Biopython, argparse and

Then you can run the script with the following command :

    python Blast_Align.py protein_uniprot_id

  Author
  ------
    Hocine Meraouna
"""

import requests as r
import argparse
import os
from Bio import SeqIO
from io import StringIO
from Bio.Blast import NCBIWWW

BASEURL="http://www.uniprot.org/uniprot/"

def get_fasta(prot_id):
    """
    """
    print('1)- Getting the fasta sequence :')

    currentUrl=BASEURL+prot_id+".fasta"
    response = r.post(currentUrl)
    cData=''.join(response.text)

    Seq=StringIO(cData)

    print('Done.')

    return list(SeqIO.parse(Seq,'fasta'))

def run_blastp(sequence, cID, RES_PATH):
    """
    """
    print('2)- Running Blastp :')
    
    # note to myself, don't forget to add :
    # database and hitlist_size as arguments for the user
    result_handle = NCBIWWW.qblast("blastp", "swissprot", sequence)

    print('writing on xml file')

    if not os.path.exists(RES_PATH):
        os.makedirs(RES_PATH)

    with open(RES_PATH+cID+"_blastp.xml", "w") as out_handle:
        out_handle.write(result_handle.read())

    result_handle.close()

    dico = {}

    print('writing in fasta format')

    with open(RES_PATH+cID+"_blastp.xml", 'r') as blast_file:
        for line in blast_file:
            if line.strip().startswith('<Hit_def>'):
                k = '>'+line.split('>')[1].split('<')[0]
                if '&gt' in k:
                    k = k.split('&gt')[0]
            if line.strip().startswith('<Hsp_qseq>'):
                if 'RecName: Full=' in k:
                    k = '>'+k[15:]
                dico[k.strip()] = line.split('>')[1].split('<')[0]
                #print(line.split('>')[1].split('<')[0])

    #print(dico)

    fasta_seq = open(RES_PATH+cID+'_HomolSeq.fasta', 'w')
    for k in dico:
        fasta_seq.write(k)
        fasta_seq.write('\n')
        fasta_seq.write(dico[k].replace("\n", ""))
        fasta_seq.write('\n\n')

    fasta_seq.close()

    print('Done.')

if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("protID", help="the uniprot id of the protein", type=str)

    ARGS = PARSER.parse_args()

    PID = ARGS.protID

    run_blastp(get_fasta(PID)[0].seq, PID)
