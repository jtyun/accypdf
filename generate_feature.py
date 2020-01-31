# -*- coding: utf-8 -*-
"""
@author: Yong Chen
"""

# Import libraries 
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
from nltk.tokenize import word_tokenize
import string
import numpy
import pandas as pd

# %%
    
table_pages_location=input("Enter table folder location : ") 
non_table_pages_location=input("Enter non-table folder location : ") 


# function of extracting text from pdf through images
def extract_text(pdf_path):
    # pdf_path is the signle pdf file name
    # Convert pdf into images file
    pages= convert_from_path(pdf_path)
    image_counter = 1
    # Iterate all pages in the pdf file and store the new images file
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG') 
        image_counter = image_counter + 1
    
    # Extract text from images
    filelimit = image_counter-1
    for i in range(1, filelimit + 1): 
        filename = "page_"+str(i)+".jpg"
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        text = text.replace('-\n', '') 
    
    return text
        
        
# Generate text data    
table_list=[extract_text(os.path.join(table_pages_location,filename)) for filename in os.listdir(table_pages_location)]

non_table_list=[extract_text(os.path.join(non_table_pages_location,filename)) for filename in os.listdir(non_table_pages_location)]
 
    

# Functions of features
def empty_rows(text):
    if text==0:
        return 0
    else:
        return text.count('\n\n')   #issue of cannot count the whitespace

def rows(text):
    if text==0:
        return 0
    else:
        return text.count('\n')   

def num_ratio(text):
    #convert pdf file to text
    # If text=0, means they are just a picture without table
    if text==0:
        num_ratio=0
    else:
        #remove punctuation 
        clean_text=text.translate(str.maketrans('', '', string.punctuation))
        #split words
        separated_words = word_tokenize(clean_text)
        #Distinguish numbers and calculte ratio
        num_ratio=len([x for x in separated_words if x.isdigit()])/len(separated_words)
    return num_ratio

def dollar_count(text):
    if text==0:
        return 0
    else:
        return text.count('$')
    

def generate_feature(text):
    return empty_rows(text), rows(text), num_ratio(text), dollar_count(text)
    
    
# can count for ''
    
# Replace empty cells in the list with 0

for i in range(len(non_table_list)):
    if non_table_list[i]=='':
        non_table_list[i]=0

print('Generating features.')

# Calculate features 

T_data=pd.DataFrame((generate_feature(i) for i in table_list),columns=['empty_rows','rows', 'num_ratio','dollar_count'])
N_data=pd.DataFrame((generate_feature(i) for i in non_table_list),columns=['empty_rows','rows', 'num_ratio','dollar_count'])

# add one table column, with value 1 indicating tables, 0 indicating non-tables

T_data['Table']=numpy.repeat(1,len(table_list))
N_data['Table']=numpy.repeat(0,len(non_table_list))

# Combine two dataframes

data=pd.concat([T_data, N_data])

data.to_csv('pdf_data.csv')

print('Generated data')

# Will try to figure out how to calculate the actual whitespaces



#%% Machine learning algorithms
