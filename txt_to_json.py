from collections import defaultdict
from nltk.tokenize import word_tokenize, sent_tokenize
import string
import nltk
import re
import math
import json
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer




def clean(text):

    # Expand contractions
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"'s", " 's", text)
    text = re.sub(r"'m", " am", text)
    text = re.sub(r"'re", " are", text)
    text = re.sub(r"'ll", " will", text)
    text = re.sub(r"'ve", " have", text)
    text = re.sub(r"'d", " would", text)

    # remove numbers
    text = re.sub(r"\b\d+'\bd\b", "", text)

    # Remove Arabic text and keep only English text
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    return text


def processYear(i, num_lines, lines):
    reviews = defaultdict(list)

    while i < num_lines-2:
        line = lines[i].strip()  # Remove leading and trailing whitespaces
        type, book_name = line.split(':', 1) #bookname
        i += 2  # skip the review id
        line = lines[i].strip()  # Remove leading and trailing whitespaces
        # for each book
        doc = ""
        while line != '----------------------------------------':
            # eat all the stuff, including id and book reviews:
            # we delete them in stop words
            doc += clean(line + " ")
            if line.find("days.This") != -1:
                print(line)
            i += 1
            line = lines[i].strip()
            
        reviews[book_name] = doc
        i += 1  # skip Year:
  

    return reviews



def extract_books_reviews(file_path, word_dict):

    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines into a list
        num_lines = len(lines) 
        i = 0  
        # while i < num_lines:
        line = lines[i].strip()  # Remove leading and trailing whitespaces
        type, text = line.split(':', 1)
        return processYear(i+1, num_lines, lines)
    
def extract_books_summaries(file_path, word_dict):

    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines into a list
        num_lines = len(lines) 
        i = 0  
        # while i < num_lines:
        line = lines[i].strip()  # Remove leading and trailing whitespaces
        type, text = line.split(':', 1)
        return processYear(i+1, num_lines, lines)
    

def extract_books_summaries(file_path, word_dict):
    book_summary = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines into a list
        num_lines = len(lines) 
        i = 0  
        while i < num_lines:
            line = lines[i].strip()  # Remove leading and trailing whitespaces
            if line.find("book name") != -1:
                type, text = line.split(':', 1)
                book_name = text
                i += 1
                line = lines[i].strip()
                type, text = line.split(':', 1)
                if type == "book summary":
                    book_summary[book_name] = text
                    i += 1
                    line = lines[i].strip()
                    while line != '----------------------------------------':
                        book_summary[book_name] += line
                        i += 1
                        line = lines[i].strip()
            i += 1

    return book_summary


def main():

    word_dict = defaultdict(int)
    # book_reviews = extract_books_reviews("2020-2022reviews.txt", word_dict)
    book_summaries = extract_books_summaries("2020-2022summaries.txt", word_dict)

    # dict: book1:reviews, book2:reviews

    with open('2020-2022summaries.json', 'w', encoding= 'utf-8') as jsonfile: 
        json.dump(book_summaries, jsonfile, indent=4, ensure_ascii=False)
        # json.dump(book_reviews, jsonfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()


