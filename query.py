import time

def findIntersections(): #Returns list of intersect docIDs


def findURLs():
    stemTokens = open("stemmer.txt", 'r')
    stem_text = stemTokens.read()
    stems_dict = eval(stem_text)
    stemTokens.close()

    docID = open("docID.txt", 'r') #{URL: docID}
    docID_text = docID.read()
    docID_dict = eval(docID_text) #Dictionary {URL: docID}

    URLs = []

    for token in terms:
        stem = stems_dict[token]
        docIDs = docID_dict[stem]
        totalResult[token] = docIDs

    beginTimer = time.time() #Start Query Time
    docID_lst = findIntersections() #Find docIDs
    lsts = docID_dict.values()
    result = set(lsts[0]).intersection(*lsts)
    for docID in docID_lst:
        url = docID_dict[docID]
        URLs.append(url)
    stopTimer = time.time()
    totalTime = stopTimer - beginTimer


if __name__ == "__main__":


    #tokenDocID = open("tokenDocID.txt", 'r')
    #docID_text = tokenDocID.read()
    #docID_dict = eval(docID_text)
    #tokenDocID.close()

    query = str(input())
    terms = query.split()

    totalResult = {}


