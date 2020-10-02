import pandas as pd
import re
from tika import parser
import numpy as np

def extract_pdf(url):
  '''
  Name: extract_pdf
  Description: Takes user input of pdf url/link of academic paper and 
  extracts relevant information. 
  Input: 
  @url: the string of link to pdf of requested academic paper
  Output: A pandas Series with ... citations, and full body text
  '''

  # Parse PDF from url
  pdfFile = parser.from_file(url)
  text = pdfFile["content"].strip()

#   title_author = text.split(re.search('(?i)Abstract', text)[0],1)[0].strip().replace('\n\n', '\n')

  #Get ABSTRACT
  try:
    # Find keyword in text and split to remove leading whitespace after Keyword.
    search = '(?i)Abstract'
    keyword = re.search(search, text)[0]
    post_abstract = text.split(keyword,1)[1].strip()

    # Extract subtring (Abstract) until two newlines detected
    abstract = post_abstract[:post_abstract.index('\n\n')].strip()

  except:
    abstract = np.nan

  #Get CONCLUSION
  try:
    #search parameters for conclusion
    search = '(?i)(Conclusion(s)|Summary|Discussion)'

    keyword = re.search(search,text)[0]

    #split text to after keyword found
    post_conclusion = text.split(keyword,1)[1].strip()

    #index keyword 'refrences in split text containing conclusion(s)
    end = re.search('(?i)(References|Bibliiography|Works Cited|Sources|Citations)',post_conclusion).start()

    #Extract text from 'conclusion' keyword to 'references' keyword.
    conclusion = post_conclusion[:end-1].strip()
    #conclusion = post_conclusion[:post_conclusion.index('\n\n')].strip()
  
  except:
    conclusion = np.nan

  #Get CITATIONS and FULL BODY TEXT WITHOUT CITATIONS
  try:
    # list of indicators/key words for the "citations" category 
    search = '(?i)(References|Bibliiography|Works Cited|Sources|Citations)'

    #Find keyword used from list
    keyword = re.search(search,text)[0]

    #Split on keyword and extract everything after match
    citations = text.split(keyword,1)[1].strip()

    #return the full body text of the article without the citations.
    fulltext = text.split(keyword,1)[0].strip() 

    #Create Exception to remove Appendix or Acknowledgemnt section
    if (re.search('(?i)(Appendix|Acknowledgement)',citations)):

      keyword2 = re.search('(?i)(Appendix|Acknowledgement)',citations)[0]

      #citations is between 'citations' keyword and 'appendix; keyword.
      citations = citations.split(keyword2,1)[0].strip()
  
  except:
    citations = np.nan  
    fulltext = text

  #Get PUBLISHERS, UNIVERSITY NAME & DEPARTMENT
  #using a text file containing everything before keyword 'abstract'

  publisher = university = dept = '' #assign response variables

  # Save introduction (varaible: title_author) - all text before Abstract or 
  # first 300 characters into .txt file to save search line by line and extract 
  # single line relevant information is found.
#   try:

#     #Asssign varibles to hold search matches
#     publisher_name = []
#     university_name = []
#     dept_name = []

#     #Search critera for each response variables
#     search1= '(?i)(Journal|Review|Magazine|Periodical|Vol|IEEE|Proceedings|Conference)'
#     search2= '(?i)(University|College|Institute|Polytechnic|School|Institution)'
#     search3= '(?i)(Department|College|Faculty|School|Institution|Group)'

    # Search through text file for maatches, if match is detected, then, the 
    # line which the match is detected is 

#     for line in title_author.split('\n'):
#       if (re.search(search1, line)):
#         publisher_name.append(line.replace('\n', ''))
#       if (re.search(search2, line)):
#         university_name.append(line.replace('\n', ''))
#       if (re.search(search3, line)):
#         dept_name.append(line.replace('\n', ''))

#     # Record the first instance of a match to the reponse variable, otherwise
#     # return back all text before introduction.
#     try:
#       publisher = publisher_name[0]
#     except:
#       publisher = title_author

#     try:
#       university = university_name[0]
#     except:
#       university = title_author
    
#     try:
#       dept = dept_name[0]
#     except:
#       dept = title_author
    
    #assign all to introduction text if no matches found
    # except:
        # publisher = university = dept = title_author
  
  #assign all to introduction text if no introduction scraped
#   except: pass
#     publisher = university = dept = title_author

  for data in [publisher, university, dept, abstract, conclusion, citations, fulltext]:
    if type(data) == str:
      data = data.replace('\n', '')
    
  results = pd.Series({
                          # 'Title & Author': [title_author.replace('\n\n', '')],
                          # 'Publication Year': [year],
                          'Publisher': publisher,
                          'University Name': university,
                          'University Department': dept,
                          'Abstract': abstract,
                          'Conclusion': conclusion,
                          'Citations': [citations], # needs to change
                          'Text': fulltext
                          })

  return results
