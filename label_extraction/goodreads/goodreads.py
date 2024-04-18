import nltk
from collections import defaultdict
from nltk.tokenize import word_tokenize
from transformers import BartForSequenceClassification, BartTokenizer
import collections
import spacy
import math
from tf_idf import calculate
# import phrasemachine
import re
from nltk.corpus import stopwords
nlp = spacy.load("en_core_web_sm")

# connect with tfidf
# nltk.data.path.append('/Users/zedongchen/nltk_data/stopwords')
# nltk.download()
# nltk.download('punkt')

nltk.download('stopwords')


import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    print(type(data))
    return data




def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    with open('remove_words.txt', 'r') as file:
        for line in file:
            stop_words.add(line.strip())
    replacements = {
        'New York': 'NewYork',
        'New york Times': 'NewYorkTimes',
        'Statue of Liberty': 'StatueofLiberty'
    }
    # 替换函数
    def replace_phrases(text, replacements):
        for old, new in replacements.items():
            text = re.sub(r'\b' + re.escape(old) + r'\b', new, text)
        return text
    # 应用替换
    text = replace_phrases(text, replacements)
    # 1. Remove punctuation

    doc = nlp(text)
    tokens = [token.text for token in doc]
    pos = [token.pos_ for token in doc]
    # print(pos)
    nouns = []
    adjs = []
    verbs = []
    # diction = phrasemachine.get_phrases(tokens=tokens, postags=pos)
    for i in range(len(pos)):
        if tokens[i].lower() not in stop_words:
            if pos[i] == "NOUN":
                nouns.append(tokens[i])
            elif pos[i] == "VERB":
                verbs.append(tokens[i])
            elif pos[i] == "ADJ" or pos[i] == "ADV":
                adjs.append(tokens[i])
    # print(nouns,adjs,verbs)
    return nouns, adjs,verbs


def summary_to_categories(file_name):
    data = read_json(file_name)
    word_dictionary = collections.defaultdict(int)
    for key, value in data.items():
        if value:
            # print(value)
            # break
            summary = value
            nouns, adjs,verbs = preprocess_text(summary)
            for word in nouns:
                word_dictionary[word] += 2
            for word in adjs:
                word_dictionary[word] += 0.5
            for word in verbs:
                word_dictionary[word] += 0.5


    result = calculate(data, word_dictionary)

    return result[200:]
    # return None
        
        
file_name = "GoodRead_books_summary.json"
sorted_words = summary_to_categories(file_name)
with open('categories_goodreads.txt', 'w') as file:
    for word in sorted_words:
        file.write(word[0] +"\t" + str(word[1])+ "\n")
