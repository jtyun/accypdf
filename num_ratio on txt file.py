# -*- coding: utf-8 -*-

#Based on txt file
import re
import string
import nltk
from nltk.tokenize import word_tokenize

def num_ratio(path):
    #read in the test data line by line(list of each line)
    filename= path
    lineList = [line.rstrip('\n') for line in open(filename)]
    #calculate the empty rows in the list
    empty_row_ratio=sum(x is '' for x in lineList)/len(lineList)
    # remove punctuation 
    stripped = [w.translate(str.maketrans('', '', string.punctuation)) for w in lineList]
    #split words
    separated_words = word_tokenize(' '.join(stripped))
    #Distinguish numbers and calculte ratio
    num_ratio=len([x for x in separated_words if x.isdigit()])/len(separated_words)
    return empty_row_ratio,num_ratio


num_ratio('Cumberland County (ME)_FY2013-pages-40.txt')

