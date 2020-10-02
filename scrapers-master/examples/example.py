#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import scrapers
from scrapers.scrape.core import scrape_core
# from scrapers.scrape.arxiv import scrape_arxiv

# In[ ]:


kwargs = dict(query='blockchain', count=1)

scrape_core(**kwargs)

# In[ ]:


scrape_core(**kwargs)
