import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import BartForSequenceClassification, BartTokenizer
import collections
import spacy
import phrasemachine
import re
from tf_idf import calculate
nlp = spacy.load("en_core_web_sm")
nltk.download('punkt')
nltk.download('stopwords')

import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    print(type(data))
    return data


def make_twitter_diction(twitter_json_file):
    twitter_data = read_json(twitter_json_file)
    twitter_all_summaries  = {}
    for book_name,content in twitter_data.items():
        twitter_all_summaries[book_name] = content[0]["summary"] if len(content) >= 1 else ""
    return twitter_all_summaries


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
    doc = nlp(text)
    tokens = [token.text for token in doc]
    pos = [token.pos_ for token in doc]
    nouns = []
    adjs = []
    verbs = []
    for i in range(len(pos)):
        if tokens[i].lower() not in stop_words:
            if pos[i] == "NOUN":
                nouns.append(tokens[i])
            elif pos[i] == "VERB":
                verbs.append(tokens[i])
            elif pos[i] == "ADJ" or pos[i] == "ADV":
                adjs.append(tokens[i])
    return nouns, adjs,verbs

def summary_to_categories(twitter_json_file):
    word_dictionary = collections.defaultdict(int)
    twitter_all_summaries = make_twitter_diction(twitter_json_file)
    for book_name, summary in twitter_all_summaries.items():
            nouns, adjs,verbs = preprocess_text(summary)
            for word in nouns:
                word_dictionary[word] += 2
            for word in adjs:
                word_dictionary[word] += 0
            for word in verbs:
                word_dictionary[word] += 0
    # sorted_words = sorted(word_dictionary.items(), key=lambda x: x[1], reverse=True)
    sorted_words = calculate(twitter_all_summaries,word_dictionary)
    print(len(sorted_words))
    # print(len(sorted_words))
    return sorted_words

twitter_file_name = "twitter.json"
sorted_words = summary_to_categories(twitter_file_name)
sorted_words = sorted_words[:200]
with open('categories_twitter.txt', 'w') as file:
    for word in sorted_words:
        file.write(word[0] +"\t" + str(word[1])+ "\n")
