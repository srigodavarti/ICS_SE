import mmap
import re
import os
import json
import glob
import sys
import html
from html.parser import HTMLParser
# import _pickle as pickle
import pickle
from urllib.request import urlopen
from bs4 import BeautifulSoup
# from urllib2 import Request, URLError, HTTPError
from urllib.request import Request
from urllib.error import URLError, HTTPError
import nltk
# nltk.download('punkt')
from nltk import word_tokenize, sent_tokenize
from lxml.html import fromstring
from nltk.stem import PorterStemmer



class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None


# As we are using tokens with length being >=2, the stop words are ammended accordingly
stop_words = ['about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren",
              'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
              "can", 'cannot', 'could', "couldn", 'did', "didn", 'do', 'does', "doesn", 'doing', "don",
              'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn", 'has', "hasn", 'have',
              "haven't", 'having', 'he', 'her', 'here', 'hers', 'herself', 'him',
              'himself', 'his', 'how', "how's", 'if', 'in', 'into', 'is',
              "isn", 'it', 'its', 'itself', 'me', 'more', 'most', "mustn", 'my', 'myself',
              'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our',
              'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she',
              'should', "shouldn", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs',
              'them', 'themselves', 'then', 'there', 'these', 'they',
              'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn",
              'we', 'were', "weren", 'what', 'when',
              'where', 'which', 'while', 'who', 'whom', 'why', 'with', "won",
              'would', "wouldn", 'you', "ll", "re", "ve", 'your', 'yours', 'yourself',
              'yourselves']

index = {}  # soon we can initialize this to have default value of empty linked list.
stemmer_dict = {}
assigned_doc_id = {}  # dict of filename to docID





def get_content(file_path, docID):
    f = open(file_path)
    data = json.load(f) #store JSON dictionary in data
    soup = BeautifulSoup(data["content"], "lxml") #Extract lxml "content" from JSON
    for tag in soup.find_all(['script']): #Extract all tags in <script> tag
        tag.extract() #Extract content between tags


    file_content = soup.get_text(" ")
    file_content_tokens = tokenize(file_content, f, docID, "file content")

    # find text within tags with higher weight
    weighted_content = soup.find_all(['h1', 'h2', 'h3', 'b'], text=True)
    weighted_content = ' '.join([e.string for e in weighted_content])
    weighted_content_tokens = tokenize(weighted_content, f, docID, "weighted content")

    return file_content_tokens, weighted_content_tokens


#RETURNS DICTIONARY FOR ONE FILE
def tokenize(text, file, docID, content_type): #Tokenizing JSON file {tokens, (frequency, firstPosition, docID, content_type)}
    ps = PorterStemmer()
    """ converts JSON file to list of tokens """
    file_tokens = dict()
    tokens = re.split('[^A-Za-z0-9]+', text.lower()) #Split by anything NOT alphanumeric
    tokens = [token.lower() for token in tokens if not token.isdigit() and token not in stop_words] #Delete only digits
    for token in tokens: #Iterate tokens in 1 file
        stemmer_dict[token] = ps.stem(token)
        token_stem = ps.stem(token) #Stem token before storing in index
        if len(token) >= 2:
            if token_stem in file_tokens.keys(): #If token already counted
                freq = file_tokens[str(token_stem)][0] #Get frequency
                position = file_tokens[str(token_stem)][1]
                tpl = (freq + 1, position, docID, content_type)
                file_tokens[str(token_stem)] = tpl #Increase frequency
            if token_stem not in file_tokens.keys():
                position = text.lower().index(str(token))
                file_tokens[str(token_stem)] = (1, position, docID, content_type)
    return file_tokens #{tokens, (frequency, position, docID, content_type)}


def update_index(token_dict):
    for token in token_dict.keys():
        if token not in index:
            lst = [token_dict[token]]
            index[token] = lst
        else:
            docID = index[token]
            index[token].append(token_dict[token])
            curr = index[token].head
            while (curr.next and curr.value < docID):
                curr = curr.next
                curr.next = Node(docID)


def clear_index():
    index.clear()


def print_index(count):
    outputFile = open("tokenOutput" + str(count) + ".txt", 'a+', encoding="utf-8")
    for token in index:
        outputFile.write(str(token).rstrip('\n'))
        outputFile.write(": ")
        printval = index[token].head
        while printval is not None:
            outputFile.write(str(index[token]))
            outputFile.write("->".rstrip('\n'))
            printval = printval.next
        outputFile.write("\n")
    outputFile.close()

def print_index_final(): #Index = {tokens, (docID, frequency)}
    outputFile1 = open("finalIndex3.txt", 'a+', encoding="utf-8")
    for token in index:
        documentCount = 0
        document = index[token].head
        while document is not None:
            documentCount = documentCount + 1
            document = document.next
        outputFile1.write(token + ":" + str(len(index[token])) + '\n')
    outputFile1.close()

def print_entire_index():
    indexOutput = open("finalIndex.txt", 'a+', encoding="utf-8")
    indexOutput.write(str(index))
    indexOutput.close()
    tokenStem = open("stemmer.txt", 'a+', encoding="utf-8")
    tokenStem.write(str(stemmer_dict))
    tokenStem.close()


def print_id():
    outputFile2 = open("documentIDs.txt", 'a+', encoding="utf-8")
    outputFile2.write(str(assigned_doc_id))
    outputFile2.close()



def indexify():
    """ turns a list of JSON files into an inverted index """
    directoryCount = 0
    fileCount = 0
    totalTokenCount = 0
    docID = 1
    threshold = 0
    cwd = os.getcwd()

    for root, directory, files in os.walk('DEV'):
        directoryCount = directoryCount + 1 # Count directories
        folderPath = cwd + "/" + root
        for file in files:
            fileCount = fileCount + 1 # Count files
            filePath = folderPath + "/" + file
            if filePath.endswith('.json'):
                print(filePath) #Print opened file


                file_tokens, weighted_tokens = get_content(filePath, docID) #Dictionary per File {tokens, (frequency, position, docID, content_type)}
                totalTokenCount = totalTokenCount + len(file_tokens) + len(weighted_tokens)
                doc_info = (docID, totalTokenCount)
                assigned_doc_id[filePath] = doc_info
                update_index(file_tokens)
                update_index(weighted_tokens)

                threshold = len(index.keys())
                if threshold >= 300000:
                    outputFileCount = outputFileCount + 1
                    print_index(outputFileCount)
                    threshold = 0

                docID = docID + 1
            print(fileCount)
            print(totalTokenCount)
    return fileCount, totalTokenCount

def printResults(fileCount, totalTokenCount):
    outputFile3 = open("RESULTS.txt", 'a+', encoding="utf-8")
    outputFile3.write("File Count: " + str(fileCount) + '\n')
    outputFile3.write("Total Tokens Count: " + str(totalTokenCount) + '\n')
    outputFile3.close()




if __name__ == "__main__":
    fileCount, totalTokenCount = indexify()
    print(fileCount) #55,394 #55394
    #print(fileTokenCount) #10,303,470
    #print(weightedTokenCount) #518,179
    print(totalTokenCount) #10,821,649 #10,275,449
    print_entire_index()
    printResults(fileCount, totalTokenCount)
    print_id()

