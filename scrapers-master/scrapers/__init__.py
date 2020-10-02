#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import logging

logger = logging.getLogger(name='error_logger')
# formatter = logging.Formatter('%(asctime)s %(message)s')
# logger.setFormatter(formatter)
logger.setLevel(logging.DEBUG)

filehandler = logging.FileHandler('log.txt')
filehandler.setLevel(logging.DEBUG)
# filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

print('Starting log')
