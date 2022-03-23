# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 12:05:29 2022

@author: LSM5
"""

"""
This file aim to provide all the usual preprocessing funtions that can be used to tockenise an clean
a given text

"""


import nltk
import spacy
import unicodedata
from nltk.stem import PorterStemmer
from nltk.tokenize.toktok import ToktokTokenizer
from pprint import pprint
import numpy as np
import re
from tqdm import tqdm


# =============================================================================
# 
# TOKENAZATION
# 
# =============================================================================

tokenizer = ToktokTokenizer()
#words = tokenizer.tokenize(sample_text)


# =============================================================================
# 
# REMOVE ACCENTED CHARACTERS
# 
# =============================================================================

def rmv_accent_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text



# =============================================================================
# 
# REMOVE SPECIAL CHARS
# 
# =============================================================================

def rmv_special_chars(text, rmv_nums=False):
    pattern = r'[^a-zA-z&0-9\s]' if not rmv_nums else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    
    # remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # remove extra newlines
    text = re.sub(r'[\r|\n|\r\n]+', ' ',text)
    
    return text



# =============================================================================
# 
# CASE CONVERSION
# 
# =============================================================================

#text.lower()


# =============================================================================
# 
# STEMMING
# 
# =============================================================================

def text_stemming(text):
    ps = PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text


# =============================================================================
# 
# LEMMATIZATION
# 
# =============================================================================

def lemmatize_text(text):
    nlp = spacy.load('en_core_web_sm')
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text

lemmatize_text("marmite")

# =============================================================================
# 
# REMOVE UNUSEFUL WORDS (adv, conj, etc)
# 
# =============================================================================

def rmv_stopwords(text, is_lower_case=False):
    stopwords = nltk.corpus.stopwords.words('english')
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopwords]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopwords]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text




def preprocess_text(text_list, rmv_accent_char=True, to_lower_case=True, lemma=True,
                    rmv_special_char=True, rmv_stopword=True, rmv_nums=True):
    
    preprocessed_texts = []
    
    # normalize each text in the textlist
    for text in tqdm(text_list):

        # remove accented characters
        if rmv_accent_char:
            text = rmv_accent_chars(text)
       
        # lowercase the text    
        if to_lower_case:
            text = text.lower()
            
        # lemmatize text
        if lemma:
            text = lemmatize_text(text)
            
        # remove special characters and\or digits    
        if rmv_special_char:
            # insert spaces between special characters to isolate them    
            special_char_pattern = re.compile(r'([{.(-)!}])')
            text = special_char_pattern.sub(" \\1 ", text)
            text = rmv_special_chars(text, rmv_nums=rmv_nums)  
       
        # remove stopwords
        if rmv_stopword:
            text = rmv_stopwords(text, is_lower_case=to_lower_case)
            
        preprocessed_texts.append(text)
    
    return preprocessed_texts