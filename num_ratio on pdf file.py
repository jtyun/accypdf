# -*- coding: utf-8 -*-

#Based on pdf file
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

#convert pdf file to text using pdfminer
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

#issue:word and number stick together  
    
def num_ratio(path):
    #convert pdf file to text
    #remove punctuation 
    text=convert_pdf_to_txt(path).translate(str.maketrans('', '', string.punctuation))
    #split words
    separated_words = word_tokenize(text)
    #Distinguish numbers and calculte ratio
    num_ratio=1-(len([x for x in separated_words2 if x.isalpha()])/len(separated_words2))
    return num_ratio

num_ratio('Cumberland County (ME)_FY2013-pages-40.pdf')
