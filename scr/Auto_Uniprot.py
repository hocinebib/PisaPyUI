#!/usr/bin/python3
"""
Code to get uniprot id of the protein and download it's fasta sequence

  How to use
  ----------
First you need to have the python packages selenium, 

Then you can run the script with the following command :

    python auto_uniprot.py "MexA MexB OprM"

  Author
  ------
    Hocine Meraouna

"""

import argparse
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

def start():
    """
    The function to access to the uniprot website
    
    Parameters
    ----------
    None
    
    Returns
    -------
    selenium webdriver
    """

    print("1- Accessing to Uniprot website :")

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.uniprot.org/")

    print("Done.")

    return driver


def uniprot_id(driver, protein):
    """
    """
    print("2- Finding uniprot id for "+protein+" :")
    prot_entry = driver.find_element_by_name("query")
    prot_entry.clear()
    prot_entry.send_keys(protein.lower())

    driver.find_element_by_id("search-button").click()

    driver.find_element_by_xpath("//select[@name='limit']/option[text()='250']").click()

    results = driver.find_elements_by_class_name('protein_names')

    for i, hit in enumerate(results):
        if protein.lower() in hit.text.lower():
            break

    name = driver.find_elements_by_class_name('entryID')

    return name[i].text


def download_fasta(fasta_name):
    """
    """

    url = 'https://www.uniprot.org/uniprot/'+fasta_name+'.fasta'
    r = requests.get(url, allow_redirects=True)

    open(fasta_name+'.fasta', 'wb').write(r.content)


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("protein_names", help="list of protein names", type=str)

    ARGS = PARSER.parse_args()

    PROT_NAMES = ARGS.protein_names

    browser = start()

    for p in PROT_NAMES.split():
        download_fasta(uniprot_id(browser, p))

    browser.close()
