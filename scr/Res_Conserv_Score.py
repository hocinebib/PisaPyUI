#!/usr/bin/python3
"""
Conservation score using JS Divergence Scoring method with compbio.cs.princeton.edu.

  How to use
  ----------
First you need to have the python packages .

Then you can run the script with the following command :
    python Res_Conserv_Score.py full_path_multialign_fasta_file

  Author
  ------
    Hocine Meraouna
"""

import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import os


def start():
    """
    """
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    driver.get("https://compbio.cs.princeton.edu/conservation/score.html")

    return driver

def launch_score_calculation(driver, alignment_file, prot, RES_PATH):
    """
    """
    url = driver.current_url

    driver.find_element_by_name("align_file").send_keys(alignment_file)

    driver.find_element_by_xpath("//input[@type='submit']").click()

    new = driver.current_url

    while new == url:
        new = driver.current_url

    with open(RES_PATH+prot+'_'+new.split('/')[-1].split('.')[-2]+'.txt', 'w') as f:
        f.write(driver.page_source)

    return RES_PATH+prot+'_'+new.split('/')[-1].split('.')[-2]+'.txt'

def score_csv(score_file):
    """
    """
    dico = {'res': [], 'conservation score': []}
    i = 1

    with open(score_file, 'r') as f:
        for line in f:
            if (line[0] not in ['<', '#', '\n']) and (line.split()[-1][0] != '-'):
                dico['res'].append(line.split()[-1][0]+' '+str(i))
                i += 1
                dico['conservation score'].append(line.split()[1])

    return dico


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("mul_ali_file", help="the multiple alignment file with full path", type=str)

    ARGS = PARSER.parse_args()

    MUL_ALI_FILE = ARGS.mul_ali_file

    pd.DataFrame.from_dict(score_csv(launch_score_calculation(start(), MUL_ALI_FILE, 'test'))).to_csv(MUL_ALI_FILE.split('/')[-1].split('.')[-2]+'.csv')
