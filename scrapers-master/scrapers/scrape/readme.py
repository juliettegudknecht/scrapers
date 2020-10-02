#!/usr/bin/env python
# coding: utf-8

# 
# # Scrape
# 
# ### Modules:
# - [google_scholar](#google) (scrape_google_scholar from Task 2 Stage 1)
# - core (scrape_core from Task 9 Stage 1)
# - elsevier (scrape_elsevier from Task 13 Stage 1 / Task 15 Stage 2?)
# - arxiv (scrape_arxiv from Task 10 Stage 1)
# 
# [other Stage 2 tasks to add later]
# - nasa
# - ieee
# - springer
# - crossref
# - jstor
# - hathitrust
# - europeana
# - medical / ncbi.nih.gov
# - plos
# - wiley
# 
# <br> 
# 
# #### **core.py**
# example use:
# 
# ``` scrape_core(query='blockchain', count=1, start_year=2019) ```
# 
# Requires API key? **Yes**
# 
# example output:
# 
# | Link | Title | Accessible | Page | Publish year| Authors | Publisher | Citations |
# | - | - | - | - | - | - | - | - |
# | NaN | Blockchain, Bitcoin and the synergy between IC... | False | 1 | [LA MELIA, VITO] | NaN | [https://core.ac.uk/display/156873253?source=1... | Pisa University |
# 
# <br>
# 
# #### **wikipedia.py**
# example use:
# 
# ``` scrape_wikipedia(query='blockchain', count=1) ```
# 
# Requires API key? **No**
# 
# example output:
# 
# | Link | Title | Page | References | Reference Links | Links | Citations |
# | - | - | - | - | - | - | - |
# | https://en.wikipedia.org/wiki/Blockchain | Blockchain | 1 | A blockchain, originally block chain, is a gro... | [^ a b c d e f g h i j k "Blockchains: The gre... | [https://www.economist.com/news/briefing/21677.. | [http://www.computerworld.com.au/article/60625... |
# 
# <br>
# 
# #### **elsevier.py**
# example use:
# 
# ``` scrape_elsevier(query='blockchain', count=1)```
# 
# Requires API key? **Yes**
# 
# example output:
# 
# | Link | Title | Accessible | Page number | Publish year| Authors | Publisher | Citations |
# | - | - | - | - | - | - | - | - |
# | NaN | Blockchain, Bitcoin and the synergy between IC... | False | 1 | [LA MELIA, VITO] | NaN | [https://core.ac.uk/display/156873253?source=1... | Pisa University |
# 
# <br>
# 
# #### **arxiv.py**
# example use:
# 
# ``` scrape_arxiv(query='blockchain', count=1) ```
# 
# Requires API key? **No**
# 
# example output:
# 
# | Link | Title | Accessible | Page number | Publish year| Authors | Publisher | Citations |
# | - | - | - | - | - | - | - | - |
# | NaN | Blockchain, Bitcoin and the synergy between IC... | False | 1 | [LA MELIA, VITO] | NaN | [https://core.ac.uk/display/156873253?source=1... | Pisa University |
# 
# <br>
# 
# #### **google_scholar.py**
# example use:
# 
# ``` scrape_core(query='blockchain', pages=2, start_year=2019) ```
# 
# Requires API key? **No**
# 
# example output:
# 
# | Link | Title | Accessible | Page number | Publish year| Authors | Publisher | Citations |
# | - | - | - | - | - | - | - | - |
# | NaN | Blockchain, Bitcoin and the synergy between IC... | False | 1 | [LA MELIA, VITO] | NaN | [https://core.ac.uk/display/156873253?source=1... | Pisa University |
