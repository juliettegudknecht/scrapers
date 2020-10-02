#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import numpy as np
import traceback
# from unicodedata import normalize
from scholarly import scholarly, ProxyGenerator
import sys, traceback
from fp.fp import FreeProxy

def scrape_scholar(query, pages=0, max_proxy_tries=5):
    '''  
    Name: scrape_scholar
    Description: Searches Google Scholar using query and returns data for results.
    Input:
    @query: search term
    @pages: number of pages (10 articles per page) to request
    @start_year: minimum number of words in body of text
    @log_path: file path for where to create log file
    Output: A pandas DataFrame with one paper per row
    '''

    generator = FreeProxy(rand=True)

    page_size = 10

    # create log file to write errors to
    log = open(f'{query}' + log_path + '.txt', 'w+')

    # initialize list which will contain all article data and be used for DataFrame
    rows = []

    # the number of the current result being pulled from google scholar
    index = 0

    results = str(1)
    
    num_tries = 0
    while num_tries<max_proxy_tries:
        # try-catch block that allows errors to be written in log file if they occur
        try:
            # proxy = generator.get()
            # print(proxy)

            # pg = ProxyGenerator()
            # pg.SingleProxy(http = "http://157.245.203.17:3128")
            scholarly.use_proxy(None)

            # creates a generator object for results for the query
            results = scholarly.search_pubs(query) #, start=0)

            # detects whether the limit has been passed, if there is one
            while not pages or index<page_size*pages:

                result = next(results)

                # retrieves current results object
                curr_result_bib = result.bib

                #instantiates current row container
                row = dict()

                # passes link to article
                row['Link'] = curr_result['url'] if 'url' in curr_result else np.nan

                # title of paper, removes quotes at the start and end if there
                row['Title'] = curr_result['title'] if 'title' in curr_result else np.nan

                # True if pdf is available, False otherwise
                # row['Accessible'] = bool(paper['repositoryDocument']['pdfStatus'])

                # page number paper would be on on the website assuming 10 papers per page
                row['Page number'] = index//page_size + 1

                # list of [initials last-name]
                row['Authors'] = curr_result['author'] if 'author' in curr_result else np.nan
                
                # checks published year
                row['Publish year'] = int(curr_result['year']) if 'year' in curr_result else np.nan

                # number of citations
                row['Citations'] = curr_result['cites'] if 'cites' in curr_result else np.nan

                # links to related articles
                row['Related articles'] = 'https://scholar.google.com/scholar?q=related:' + results['url_scholarbib'].split(':')[1] + ':scholar.google.com/&scioq=' + query + '&hl=en&as_sdt=0,14'

                # checks if publisher is available
                row['Publisher'] = curr_result['venue'] if 'venue' in curr_result else np.nan

                rows.append(row)
                index += 1
            # returns pandas DataFrame where each row is 1 paper
            return pd.DataFrame(rows)

        # write any errors to log file
        except Exception as e:
            # log.write(str(e))
            # print(str(e))
            # traceback.print_exc(file=sys.stdout)
            # log.write('\n')
            if rows:
                return pd.DataFrame(rows)
            if str(e) == "Cannot fetch the page from Google Scholar.":
                num_tries += 1
                continue
            else:
                return pd.DataFrame(rows)
    # returns partially filled DataFrame if failed
    return pd.DataFrame(rows)
