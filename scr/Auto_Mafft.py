#!/usr/bin/python3
"""
Code to get MAFFT multialignment

  How to use
  ----------
First you need to have the python packages selenium, 

Then you can run the script with the following command :

    python auto_mafft.py /home/meraouna/00_BioInfo/test/uniprot/P52477_Homologous_sequences_MAFFT.fasta

  Author
  ------
    Hocine Meraouna

"""

import argparse
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def getDownLoadedFileName(waitTime, driver):
    """
    function made by supputuri
    from stackoverflow :
    https://stackoverflow.com/questions/34548041/selenium-give-file-name-when-downloading
    """
    driver.execute_script("window.open()")
    WebDriverWait(driver,10).until(EC.new_window_is_opened)
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("about:downloads")

    endTime = time.time()+waitTime
    while True:
        try:
            fileName = driver.execute_script("return document.querySelector('#contentAreaDownloadsView .downloadMainArea .downloadContainer description:nth-of-type(1)').value")
            if fileName:
                return fileName
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break


def start(RES_PATH):
    """
    The function to access to the pisa web server.
    I'm using firefox but it can be changed for other browsers.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    selenium webdriver
    """
    print("1- Accessing to MAFFT website :")

    options = Options()
    options.headless = True

    profile = FirefoxProfile()
    dl_path = RES_PATH
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", RES_PATH)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                              "text/plain,text/x-csv,text/csv,application/vnd.ms-excel,application/csv,application/x-csv,text/csv,text/comma-separated-values,text/x-comma-separated-values,text/tab-separated-values,application/pdf")

    driver = webdriver.Firefox(firefox_profile=profile, options=options)

    driver.get("https://mafft.cbrc.jp/alignment/server/")

    print("Done.")

    return driver


def submit_query(driver, query_file):
    """
    """

    print("2- Submitting the fasta sequences :")

    driver.find_element_by_name("file").send_keys(query_file) #need full path

    driver.find_element_by_xpath("//input[@type='submit']").click()

    time.sleep(15)

    print('Done.')

    return driver


def download_alignment(driver, query_file, RES_PATH):
    """
    """

    driver.switch_to.frame("aframe")

    print("3- Downloading the MAFFT alignment :")

    driver.find_element_by_xpath("//*[contains(text(),'Fasta format')]").click()

    latestDownloadedFileName = getDownLoadedFileName(15, driver) #waiting to complete the download

    time.sleep(20)

    os.rename(RES_PATH+latestDownloadedFileName, '/'.join(query_file.split('/')[:-1])+'/'+query_file.split('/')[-1].split('.')[0]+'_MAFFT.fasta')

    print("Done.")

    driver.quit()


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("fasta_seq", help="fasta file with the homologous sequences given by blastp", type=str)

    ARGS = PARSER.parse_args()

    FASTA = ARGS.fasta_seq

    download_alignment(submit_query(start(), FASTA), FASTA)
