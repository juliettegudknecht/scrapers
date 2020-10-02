import pandas as pd
import numpy as np
import requests
import json

# can get api key at https://dev.elsevier.com/
api_key = '13a32fe1f557ba28e67e632957479201'
# api_key = '084d669878ab3e68b564e3f0aed17301'


def scrape_elsevier(query, count=0, start_year=None):
  '''  
  Name: scrape_elsevier
  Description: Uses Elsevier Scopus API to get papers related to query term 
  Input:
  @query: search term
  @pages: number of pages (10 articles per page) to request
  @start_year: minimum number of words in body of text
  @log_path: file path for where to create log file
  Output: A pandas DataFrame with one paper per row
  '''
  # assume scopus vs sciencedirect

  # initialize list which will contain all article data and be used for DataFrame
  rows = []

  # create or open log file to write errors to

  # calculate number of results to request
  count = 100 if count == 0 else count

  # base URL
  url = 'https://api.elsevier.com/content/search/scopus'

  # structure parameters for request
  query_data = {
      'apiKey': api_key,
      'query': query,
      'count': count
      
  }

  # adds starting year restriction to url if user designated a start year
  if start_year:
   query_data['date'] = f'{start_year}-2020'

  # makes api request to the url built above and names it response
  with requests.get(url, params=query_data) as response:

    # if a status not equal to 200 means an error occured or there are no more results to show
    if response.status_code != 200:
      return
      
    results = json.loads(response.text)
  # can use count, date, sort

    # loops through all page numbers for pages we want to scrape
    for paper in results['search-results']['entry']:

      # creates empty container to input data
      row = dict()

      # link to download paper if available
      row['Link'] = paper['link'][2]['@href'] # viewing link but not a download link
            
      # title of paper, removes quotes at the start and end if there
      row['Title'] = paper['dc:title']

      # True if pdf is available, False if not
      row['Accessible'] = paper['openaccessFlag']

      # page number paper would be on on the website assuming 10 papers per page
      row['Page'] = 1

      # list of [last-name, first name] (should we include collaborators?)
      row['Authors'] = paper['dc:creator']

      # checks published year after start_year and not a future year
      row['Year'] = int(paper['prism:coverDate'][:4])

      # number of citations
      row['Citations'] = int(paper['citedby-count'])

      # link to related articles
      row['Related'] = np.nan

      # checks if publisher is available
      row['Publisher'] = paper['prism:publicationName'] # this is journal, is publisher Elsevier?

      # DOI number which can be used to request inaccessible papers on scihub
      # row['DOI'] = paper['prism:doi'] if 'prism:doi' in paper.keys() else np.nan

      # adds paper data to our dataset
      rows.append(row)

  # returns pandas DataFrame where each row is 1 paper
  return pd.DataFrame(rows)
