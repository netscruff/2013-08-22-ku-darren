#!/usr/bin/env python
"""
fbsearch.py

Created by Darren Boss on 2013-08-21.
"""
import urllib, urllib2
from bs4 import BeautifulSoup
import argparse

def page_results(soup):
    """Return a list of names
    
    Given an instance of BeautifulSoup, will return all the names it can find
    in the search result table

    """
    result_table = soup.find('table', class_='commonTable')
    if result_table:
        scientific_names = [it.text for it in result_table.find_all('i')]
        return scientific_names
    else:
        return ["No results."]

parser = argparse.ArgumentParser(description='Return scientific names for common name.')
parser.add_argument('common_name', metavar='Common name',
                    help='Serch will be preformed for common name')
args = parser.parse_args()
# The FishBase search url
result_url = 'http://fishbase.se/ComNames/CommonNameSearchList.php'
# The common name we are serching on
common_name = args.common_name
scientific_names = []
query = {'CommonName' : common_name}
query_string = '?' + urllib.urlencode(query)
# Keep checking for the next link, when it no longer appers in the results we have
# them all
while True:
    # Concatenate parts of the url together and have open the url
    soup = BeautifulSoup(urllib2.urlopen(result_url + query_string))
    scientific_names += page_results(soup)
    # If there is an <a href=''>Next</a> tag in the results it means we don't have all
    # the results and we should also parse additional results from the next page
    next_link = soup.find('a', text='Next')
    if next_link:
	    query_string = next_link['href']
    else:
        break
for name in scientific_names:
	print name
