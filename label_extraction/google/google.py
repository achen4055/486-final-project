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
    # print(type(data))
    return data




def preprocess_text(text):
    # 1. Remove punctuation
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
    # print(pos)
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



# "12 Rules for Life: An Antidote to Chaos": {
#         "Name": "12 Rules for Life: An Antidote to Chaos",
#         "Author": "Jordan B. Peterson",
#         "User Rating": "4.7",
#         "Reviews": "18979",
#         "Price": "15",
#         "Year": "2018",
#         "Genre": "Non Fiction",
#         "ISBN": "9780345816023",
#         "google_description": "#1 NATIONAL BESTSELLER #1 INTERNATIONAL BESTSELLER What does everyone in the modern world need to know? Renowned psychologist Jordan B. Peterson's answer to this most difficult of questions uniquely combines the hard-won truths of ancient tradition with the stunning revelations of cutting-edge scientific research. Humorous, surprising and informative, Dr. Peterson tells us why skateboarding boys and girls must be left alone, what terrible fate awaits those who criticize too easily, and why you should always pet a cat when you meet one on the street. What does the nervous system of the lowly lobster have to tell us about standing up straight (with our shoulders back) and about success in life? Why did ancient Egyptians worship the capacity to pay careful attention as the highest of gods? What dreadful paths do people tread when they become resentful, arrogant and vengeful? Dr. Peterson journeys broadly, discussing discipline, freedom, adventure and responsibility, distilling the world's wisdom into 12 practical and profound rules for life. 12 Rules for Life shatters the modern commonplaces of science, faith and human nature, while transforming and ennobling the mind and spirit of its readers.",
#         "google_average_rating": 4.5,
#         "google_ratings_count": 7
#     },
def make_google_diction(data):
    google_diction = {}
    for name, content in data.items():
        if content:
            if "google_description" in content:
                google_diction[name] = content.get("google_description")
            else:
                google_diction[name] = "no"
    # print(google_diction)
    return google_diction

def summary_to_categories(google_json):
    data = read_json(google_json)
    google_data = make_google_diction(data)
    word_dictionary = collections.defaultdict(int)
    for key, value in data.items():
        # print(value)
        if value and value.get("google_description"):
            summary = value.get("google_description")
            nouns, adjs,verbs = preprocess_text(summary)
            for word in nouns:
                word_dictionary[word] += 2
            for word in adjs:
                word_dictionary[word] += 0.5
            for word in verbs:
                word_dictionary[word] += 0.5
    # sorted_words = sorted(word_dictionary.items(), key=lambda x: x[1], reverse=True)
    sorted_words = calculate(google_data,word_dictionary)
    # print(len(sorted_words))
    return sorted_words

        
        
google_json= 'google.json'
sorted_words = summary_to_categories(google_json)
with open('categories_google.txt', 'w') as file:
    for word in sorted_words:
        file.write(word[0] +"\t" + str(word[1])+ "\n")
