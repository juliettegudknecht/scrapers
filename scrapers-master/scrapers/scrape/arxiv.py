#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import pandas as pd
import pyarxiv

# In[ ]:


def scrape_arxiv(query, count=0):
  '''
  Name: scrape_arxiv
  Description: Scrapes arXiv data
  Inputs:
    @query: search term
    @count: number of articles to request
  Output: A pandas DataFrame with one paper per row
    columns: ...
  '''
  rows = []

  count = 100 if count == 0 else count

  # Get articles from arxiv
  entries = pyarxiv.query(title=query, max_results=count)

  # Search and organize publisher names from entries
  reflst = []
  for entry in entries:
    match_ = re.search("'arxiv_journal_ref': '.+?(?=',)", str(entry))
    if match_ is not None:
      reflst.append((match_.group(0))[22:])
    else:
      reflst.append("NaN")

    row = dict()
    
  # pull title, author, date, and link to PDF of paper from entries
  # and put each in its own list
    row['Link'] = entry['link'].replace("abs", "pdf")

    row['Title'] = entry['title']

    row['Page'] = 1

    row['Authors'] = entry['authors']

    row['Year'] = entry['published'][:4]
    
    row['Accessible'] = True
    
    row['Related'] = []

    rows.append(row)

  # return papers
  return pd.DataFrame(rows)
