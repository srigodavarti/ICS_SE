import math

import numpy as np


def important_content_TF_IDF():
    for token, tpl in mergeWeightDict.items():  # tuple = (Frequency, Num of Documents, 1st Position)
        tf = tpl[0] / 7000
        df = tpl[1]
        idf = tf * math.log(55395 / df + 1)
        weightedIDF[token] = idf

def file_content_TF_IDF():
    for token, tpl in mergeFileDict.items(): #tuple = (Frequency, Num of Documents, 1st Position)
        tf = tpl[0]/7000
        df = tpl[1]
        idf = tf * math.log(55395/df + 1)
        fileIDF[token] = idf

def cosineSimilarity(N, total_vocab_size):
    D = np.zeros((N, total_vocab_size))
    tf_idf = important_content_TF_IDF()
    total_vocab = file_content_TF_IDF()
    for i in tf_idf:
        ind = total_vocab.index(i[1])
        D[i[0]][ind] = tf_idf[ind]
    # cosine similarity
    Q = np.zeros((len(total_vocab)))
    counter = len(Q)



if __name__ == "__main__":
    mergeWeightedContentFile = open('mergeWeightedContentF.txt', 'r') #{token, [freq, num of doc, 1st position]}
    mergeFileContentFile = open('mergeFileContentF.txt', 'r') #{token, [(freq, position, docID, contentType)]

    weightData = mergeWeightedContentFile.read()
    mergeWeightDict = eval(weightData)
    weightedIDF = {}

    fileData = mergeFileContentFile.read()
    mergeFileDict = eval(fileData)
    fileIDF = {}

    cosineSimilarity(55394, mergeWeightDict)

    mergeWeightedContentFile.close()
    mergeFileContentFile.close()

    mergeWeightedContent = open('TF_IDF_weightedContentF.txt', 'a+', encoding="utf-8")
    mergeWeightedContent.write(str(weightedIDF))
    mergeWeightedContent.close()

    mergeFileContent = open('TF_IDF_fileContentF.txt', 'a+', encoding="utf-8")
    mergeFileContent.write(str(fileIDF))
    mergeFileContent.close()