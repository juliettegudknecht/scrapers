#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import requests
import json

from .. import logger

# api key registered at https://core.ac.uk/api-keys/register/
api_key = 'oud4CkzvaGT8fXRnPF5cBQjM3iYObwWZ'

def scrape_core(query, count=0, start_year=0):
  '''  
  Name: scrape_core
  Description: Uses CORE API to get papers related to query term 
  Input:
    @query: search term
    @count: number of articles to request
    @start_year: minimum number of words in body of text
  Output: A pandas DataFrame with one paper per row
  '''

  page_size = 10

  # initialize list which will contain all article data and be used for DataFrame
  rows = []

  if count == 0:
    page_size = 100

    # sets pages to maximum of 100 which aims to get all results
    pages = 100

  # maximum search results is 100 per request, so if less than 10 pages are requested, we can request them all in one query
  elif count <= 100:
    pages = 1
    page_size = count

  # prevents program from crashes if errors
  try:

    # loops through all page numbers for pages we want to scrape
    for page_number in range(1, pages+1):

      # add base url to search query
      core_url = 'https://core.ac.uk:443/api-v2/articles/search/' + query

      # structure parameters for requesting
      query_data = {
          'apiKey': api_key,
          'similar': 'true',
          'citations': 'true',
          'language': 'english', # does not work, but most articles are in english
          'page': page_number,
          'pageSize': page_size,
          'urls': 'true',
                    }

      # adds starting year restriction to url if user designated a start year
      if start_year:
        query_data['year'] = f'>{start_year}'

      # makes api request to the url with the parameters
      with requests.get(core_url, params=query_data) as response:

        # if a status not equal to 200 means an error occured or there are no more results to show
        if response.status_code != 200:
          break

        # turns response into a json dictionary-like object for parsing  
        results = json.loads(response.text)

      # loops through each paper in the data returns
      for i, paper in enumerate(results['data']):

        # creates empty container to input data
        row = dict()

        # link to download paper if available
        row['Link'] = paper['downloadUrl'] if paper['downloadUrl'] != '' else np.nan
        
        # title of paper, removes quotes at the start and end if there
        row['Title'] = paper['title'].strip()

        # True if pdf is available, False otherwise
        row['Accessible'] = bool(paper['repositoryDocument']['pdfStatus'])

        # page number paper would be on on the website assuming 10 papers per page
        row['Page number'] = (i // 10) + 1

        # list of [last-name, first-name]
        row['Authors'] = paper['authors']

        # checks published year after start_year and not a future year
        row['Publish year'] = int(str(paper['year'])[:4]) if len(str(paper['year'])) == 6 else np.nan#if paper['year'] >= start_year and paper['year'] <= today.year else np.nan

        # number of citations
        # row['Citations'] = len(paper['citations'])

        # links to related articles
        row['Related articles'] = [similarity['url'] for similarity in paper['similarities']]

        # checks if publisher is available
        row['Publisher'] = paper['publisher'] if 'publisher' in paper.keys() != '' else np.nan

        # adds paper data to our dataset
        rows.append(row)
    
  # write any errors to log file
  except Exception as e: logger.error(f'Could not scrape CORE for "{query}"')

  logger.debug(f'Scraped {len(rows)} articles from CORE for "{query}"')
  # returns pandas DataFrame where each row is 1 paper
  return pd.DataFrame(rows)
