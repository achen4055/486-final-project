from collections import defaultdict
from nltk.tokenize import word_tokenize, sent_tokenize
import math
from nltk.corpus import stopwords


def index_document(doc_id, content, inverted_index, vocabulary):
    """Index a document by preprocessing, tokenizing, stemming, and updating an inverted index."""
    if content:
        words = word_tokenize(content)
        vocabulary.update(set(words))
        for word in words:
            # print(word)
            if word not in inverted_index:
                inverted_index[word] = defaultdict(list)
            if doc_id not in inverted_index[word]:
                inverted_index[word][doc_id] = 1
            else:
                inverted_index[word][doc_id] = inverted_index[word][doc_id] + 1


def retrieveDocuments(inverted_index, numOfDocs, vocabulary, word_dictionary):

    terms_score = defaultdict(list)

    for term in vocabulary:
        # calculate relevant word in document
        # print(inverted_index[term])
        if term in inverted_index:
            for docID, termFrequency in inverted_index[term].items():
                # if term not in inverse_doc_frequ:
                #     # idft = log10(num of docs / document frequency of term)
                inverse_doc_frequency = math.log10((numOfDocs / len(inverted_index[term])))
                
                # instead, use new weighter term frequency
                termFrequency = word_dictionary[term]
                score = termFrequency * inverse_doc_frequency
                if term not in terms_score:
                    terms_score[term] = score
                else:
                    terms_score[term] = terms_score[term] + score
    
    return terms_score

# data:
#   data type: dictionary
#   content: {[book1 name: summary], [book2 name: summary],...}

# word_dictionary:
#   data type: dictionary
#   content: {[word1: word frequency], [word2: word frequency],...}
#   note: the words are weighted: 
#     word_dictionary[word] += 2
#     word_dictionary[word] += 0.5
#     word_dictionary[word] += 0.5

# This method will pick top 50 words among summaries in data as labels/classes/categories.
# And then it will print them out
def calculate(data, word_dictionary):

    vocabulary = set()
    inverted_index = defaultdict(list)
    numOfBooks = len(data)
    for book_name, review_content in data.items():
        index_document(book_name, review_content, inverted_index, vocabulary)

    # vocabulary = remove_stop_words(vocabulary)
    word_score = retrieveDocuments(inverted_index, numOfBooks, vocabulary, word_dictionary)
    word_counts = dict(word_score)
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Print the top 20 words and their occurrences
    # for word, count in sorted_word_counts[:50]:
    #     print(f"{word}: {count}")

    return sorted_word_counts
    
