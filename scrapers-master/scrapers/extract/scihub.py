#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup

def extract_scihub(url):
  '''
  Name: extract_scihub
  Description: Takes user url of requested academic paper and find a direct access 
  pdf link from a resource called sci-hub to bypass this. Sci-hub is essentially 
  a pirate website specifically for academic papers, books, etc. 
  Input: 
    @url: url of requested academic paper as string
  Output: string consisting of link/url to direct access pdf of 
  requested academic paper
  '''

  #create sci-hub url base for requested paper
  url='https://sci-hub.tw/'+url #all sci-hub reqiest links follow this path

  # Get response of sci-hub user requested url page,
  # Then create create soup object of Sci-Hub page.
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "lxml")

  # Extract PDF link using BeutifulSoup 
  try:
      #Scrape sci-hub page for pdf element and address
      link = soup.find("iframe", attrs={"id": "pdf"})['src'].split("#")[0]
      if link.startswith('//'): #scraping path for pdf link in sci-hub html frame
          link = link[2:]
          link = 'https://' + link
  except Exception: #error handling if link not found
      return # changed to return (None)
  
  #Return link to pdf
  return link
