#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
from bs4 import BeautifulSoup


# need to make sure it has the same outputs


def scrape_google(query: str, num_pages: int) -> pd.DataFrame:
  '''
  Name         : scrape_google
  Description  : webscrapes Google Search results given a query
  Input: 
    @query     : the string you want to google search
    @num_pages : the (int) number of Google Result pages you want to search through
  Output       : returns a pd dataframe with each search result in a row containing the title, link, and Google Result page number

  template: https://hackernoon.com/how-to-scrape-google-with-python-bo7d2tal --> https://github.com/getlinksc/scrape_google/blob/master/search.py
  '''
    # set up desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

    # initialize header values for the requests
    headers = {"user-agent": USER_AGENT}

    # removes leading and trailing whitespace and replaces all middle white space with + to fit the URL | e.g. "  computer parts  " --> "computer+parts"
    query = query.strip().replace(' ', '+')

    # by default, there are 10 results per Google Search page
    DEFAULT_NUM_RESULTS_PER_PAGE = 10
    
    # finds maximum # of results needed based on the number of pages requested
    if num_pages > 0:
      max_results = num_pages * DEFAULT_NUM_RESULTS_PER_PAGE
    # set to max # of pages, which is seemingly 25 (seems to peak in # of results found around this page number)
    else:
      max_results = 25

    # list of dictionary items that each contain the title, link, and page number for each result
    results = []

    # for loop with step size 10 b/c need to request after every 10 results to get to the next page
    for result_num in range(0, max_results, DEFAULT_NUM_RESULTS_PER_PAGE):
        URL = f"https://google.com/search?q={query}&start={result_num}"

        # performs a GET request
        resp = requests.get(URL, headers=headers)

        # checks if request has succeeded
        if resp.status_code == 200:
          
            # puts the HTML content into bs object
            soup = BeautifulSoup(resp.content, "html.parser")

            # retrives HTML elements that have <div> tag and CSS class 'r'
            for g in soup.find_all('div', class_='r'):

                # retrieves all HTML <a ... </a> tags
                anchors = g.find_all('a')

                if anchors:
                    # retrieves URL links from <a href=... </a> HTML tags
                    link = anchors[0]['href']

                    # retrieves result titles from <h3> ... </h3> HTML tags
                    title = g.find('h3').text

                    # creates item object to be appended to results list
                    item = {
                        "title": title,
                        "link": link,
                        "page": int(result_num / 10) + 1
                    }

                    results.append(item)

        # GET request status code error received
        else:
            print(f"error code: {resp.status_code}")

    # converts list to pd dataframe
    return pd.DataFrame(results) 
