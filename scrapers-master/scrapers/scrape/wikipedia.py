#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# run this first to install wikipedia package
!pip install wikipedia

# In[ ]:


import wikipedia
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random

# In[ ]:


def scrape_wikipedia(query: str, count: int) -> pd.DataFrame:
  '''
  last edit: 1:58 pm PST 9/14/2020
  
  Name         : Albert, Jackie, Sam  9/13/2020
  Description  : webscrapes Wikipedia pages given a query
  Input: 
    @query     : the search phrase you want to enter through wikipedia search
    @count         : the (int) number of Wikipedia results page you want to scrape
  Output       : returns a pd dataframe with a single row representing a single wikipedia page. The columns of this row are
                            Link = the link where you are gathering
                            Title = The title of the wikipedia article
                            Place = The place this article came up on the wikipedia search result
                            Text = the text of the wikipedia article
                            References = a list of the citations made throughout the article
                            Reference Links = a list of the links associated to the citations
                            Links = a list of links in the wikipedia article

  Wikipedia Python library documentation : https://wikipedia.readthedocs.io/en/latest/code.html
'''

  # contains URL's of the k wiki pages
  wiki_links = []

  # finds the top k titles of wiki results pages of the query and stores into list
  wiki_titles = wikipedia.search(query, count)

  # contains numerical position of query result (between 1 through k)
  wiki_place = list(range(1, count + 1))

  # contains text of the k wiki pages
  wiki_text  = []

  # contains references (list of citations) of the k wiki pages 
  wiki_references = []

  # contains reference links of the k wiki pages
  wiki_reference_links = []

  # contains links that are on the k wiki pages (not the ones in references, but in the page content)
  wiki_page_links = []

  # for each wiki page, fill out all of the remaining lists that we initialized
  for title in wiki_titles:

    ''' 
      PART 1:
        Using Wikipedia Python library to get page links, text content, and external links
    '''

    # obtains the wiki page object based on title
    try:
      wiki_page = wikipedia.page(title, auto_suggest=False) 

    # occurs when led to a Disambiguation Page, which shows several different options for a single title
    except wikipedia.DisambiguationError as e:
      
      # https://stackoverflow.com/a/50013411
      # choose a random page from the options offered by the Disambiguation Page
      selected_title = random.choice(e.options)
      wiki_page = wikipedia.page(selected_title, auto_suggest=False)

      # replace the old title in wiki_titles with the title of the randomly selected page
      wiki_titles = [selected_title if x == title else x for x in wiki_titles]

      # need to update title to selected_title for the beautifulsoup part
      title = selected_title

    # adds all the links by appending it to the base wikipedia URL and replacing all spaces between words with _
    URL = f"https://en.wikipedia.org/wiki/{title.strip().replace(' ', '_')}"
    wiki_links.append(URL)

    # retrieves all text content from the wikipedia page
    wiki_text.append(wiki_page.content)

    # retrieves all external URLs
    wiki_page_links.append(wiki_page.references)

    ''' 
      PART 2:
        Using beautifulsoup to get references and reference links 
    '''

    # set up desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

    # initialize header values for the requests
    headers = {"user-agent": USER_AGENT}

    # performs a GET request
    resp = requests.get(URL, headers=headers)

    # temp lists representing references and reference links. each represent a single wikipedia page (1 row)
    wiki_references_temp      = []
    wiki_reference_links_temp = []

    # checks if request has succeeded
    if resp.status_code == 200:
      
      # puts the HTML content into bs object
      soup = BeautifulSoup(resp.content, "html.parser")

      ''' 
        HTML Structure of Wikipedia "References" section:
        ol tag = ordered list
        li tag = list item

        <ol class="references">
          <li>
            <a class="external text" href="[reference URL here]" [reference text here] </a>

            <span class="reference-text">
              <a href="[reference URL here]" [reference text here] </a>
            </span>
          </li>
          ...
          ...
          ...
          <li>
            <a class="external text" href="[reference URL here]" [reference text here] </a>
            
            <span class="reference-text">
              <a href="[reference URL here]" [reference text here] </a>
            </span>
          </li>
        </ol>

      '''
  
      # retrieves every ol HTML tags that is from the References section
      for ol_tag in soup.find_all('ol', class_='references'):

        # retrieves every li HTML tag within each ol tag 
        for li_tag in ol_tag.find_all('li'):

          # get the reference text
          wiki_references_temp.append(li_tag.text)

          # getting the a tag to eventually get the external URL
          a_tag = li_tag.find('a', class_="external text")

          # some references don't have any external URLs
          if a_tag is None:

            # find reference with internal URL (links to other wikipedia page)
            internal_URL_soup = li_tag.find_all('span', class_="reference-text")

            if internal_URL_soup is not None:
              a_tag = internal_URL_soup[0].find('a')

            # no internal links either for this reference
            if a_tag is None:
              wiki_reference_links_temp.append('')

            # when reference has internal URL, add it as the reference link
            else:
              if a_tag['href'][0] != '#':
                wiki_reference_links_temp.append("https://en.wikipedia.org" + a_tag['href'])
              
              # when it begins with a '#', then it leads to a further citation at the bottom of the page
              # Note: we can keep going down each "#___" URL, but sometimes it keeps chaining several times, making that difficult or impossible to account for. See "Vietnam" wiki page
              else:

                # so instead, we just link to the immediate next citation thru the wiki URL (not the ideal solution)
                wiki_reference_links_temp.append(wiki_page.url + a_tag['href'])

          # when reference has external URL, add it as the reference link
          else:
            wiki_reference_links_temp.append(a_tag['href'])

      # add temp lists back to main lists (adds up all the rows together to make a column)
      wiki_references.append(wiki_references_temp)
      wiki_reference_links.append(wiki_reference_links_temp)

    # GET request status code error received
    else:
        print(f"error code: {resp.status_code}")

  # converts the lists into a formatted pd dataframe
  return pd.DataFrame(list(zip(wiki_links, wiki_titles, wiki_place, wiki_text, wiki_references, wiki_reference_links, wiki_page_links)), columns=['Link', 'Title', 'Page', 'Text', 'References', 'Reference Links', 'Links'])


# In[ ]:


scrape_wikipedia('blockchain', 2)
