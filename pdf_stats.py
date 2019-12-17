#!/usr/bin/env python
# coding: utf-8

# In[8]:


#import PyPDF2
import tika
from tika import parser
import tabula
import xml.etree.ElementTree as ET 
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from os import *
from os.path import *
import sys



# In[17]:



table_pages_location=input("Enter table folder location : ") 
non_table_pages_location=input("Enter non-table folder location : ") 

table_files=[f for f in listdir(table_pages_location) if isfile(join(table_pages_location, f))]
table_files.pop(0)   #get rid of the default value at index 0
table_files=[table_pages_location+f for f in table_files]

print("No of table pages: "+str(len(table_files)))

non_table_files=[f for f in listdir(non_table_pages_location) if isfile(join(non_table_pages_location, f))]
non_table_files.pop(0)
non_table_files=[non_table_pages_location+f for f in non_table_files]

print("No of non-table pages: "+str(len(non_table_files)))

file_list=table_files+non_table_files

non_table_indexes=['NT' for i in range(len(table_files),len(file_list))]


page_content={}

table_indexes=['T' for i in range(len(table_files))]
non_table_indexes=['NT' for i in range(len(table_files),len(file_list))]
table_ind=table_indexes+non_table_indexes

#print(file_list)

for file in file_list: 
    #file='C2016(1).pdf'                                                        #pdf file name
    raw_xml = parser.from_file(file, xmlContent=True)                          #Parse the pdf to get text in form of raw xml

    #Clean xml tags to extract text
    body = raw_xml['content'].split('<body>')[1].split('</body>')[0]
    body_without_tag = body.replace("<p>", "").replace("</p>", "").replace("<div>", "").replace("</div>","").replace("<p />","")

    #Get the text data and store it in the form of a list
    text_pages = body_without_tag.split("""<div class="page">""")[1:]   #Text data
    #num_pages = len(text_pages)      # Page numbers
    page_content["/".join(file.split('/')[-2:])]=text_pages





features=pd.DataFrame(list(page_content.items()), columns=['Pg_nm', 'Content'])
features['table_ind']=table_ind


# Function to extract the number of continuous whitespaces ith length greater than threshold.
def whitespace_counter(s,threshold):
    whites=[]
    counter=0
    s=s[0]
    for i in range(len(s)):

        if (s[i]==' '):
            counter=counter+1
            if(i==len(s)-1):
                whites.append(counter)
            continue
        if (counter!=0):
            whites.append(counter)
            counter=0
    return [i for i in whites if i>threshold]

def num_counter(s):
    s=s[0]
    #print([i for i in s])
    return sum([1 for i in s if (i.isdigit()) ])



print('Generating features.')

features['white_space_count']=features.apply (lambda x: len(whitespace_counter(x['Content'],5)), axis=1)
features['num_count']=features.apply(lambda x: num_counter(x['Content']), axis=1)
features['total_length']=features.apply(lambda x: len(x['Content'][0]), axis=1)
features['num_ratio']=features['num_count']/features['total_length']

print('Writing output file.')


features.to_csv('C:/Users/Shrilesh/Documents/pdf_extract_tables/output/pdf_stats.csv')


# In[ ]:




