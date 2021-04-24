from numpy import result_type
from numpy.core.fromnumeric import sort
import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_list = os.listdir(directory)
    file_dict = {}
    for file in file_list:
        if file.endswith(".txt"):
            f = open(os.path.join(directory,file), "r")
            file_dict[file] = f.read()
            f.close()
    return file_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = []
    for word in nltk.word_tokenize(document):
        if not all([char in string.punctuation for char in word]):
            word = word.lower()
            if word not in nltk.corpus.stopwords.words("english"):
                tokens.append(word)
    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # get all unique words in all documents
    unique_words = []
    for words in documents.values():
        if not unique_words:
            unique_words = words
        else:
            temp = [word for word in words if word not in unique_words]
            unique_words.extend(temp)
    
    # get number of documents
    docs = len(documents)

    # create dict for output mapping of words to their respective IDF values
    idf_dict = {}
    
    # iterate over words
    for word in unique_words:
        appearances = 0
        # get number of documents where the word appears
        for words in documents.values():
            if word in words:
                appearances += 1
        # assign IDF to word in output dict
        idf_dict[word] = math.log(docs/appearances)
    
    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    result_dict = {}
    # iterate over files
    for file, words in files.items():
        result_dict[file] = 0.0
        # iterate over unique words in file
        for word in query:
            # calculate tf-idf
            tfidf = idfs[word] * words.count(word)
            result_dict[file] += tfidf
    
    # sort results by tf-idf and convert to list
    tuple_list_sorted = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    result_list_sorted = [el[0] for el in tuple_list_sorted]
    return result_list_sorted[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    result_dict = {}
    # iterate over files
    for sentence, words in sentences.items():
        result_dict[sentence] = {}
        result_dict[sentence]["idf"] = 0.0
        # iterate over words in sentence
        for word in query:
            if word in words and word in idfs.keys():
                # calculate idf
                result_dict[sentence]["idf"] += idfs[word]
        # get query-term-density
        qtd = sum([1 for el in query if el in words]) / len(words)
        result_dict[sentence]["qtd"] = qtd

    # sort results by idf and qtd and convert to list
    tuple_list_sorted = sorted(result_dict.items(), key=lambda x: (x[1]["idf"], x[1]["qtd"]), reverse=True)
    result_list_sorted = [el[0] for el in tuple_list_sorted]
    return result_list_sorted[:n]


if __name__ == "__main__":
    main()
