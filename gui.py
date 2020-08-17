from tkinter import *
import time

root = Tk()
root.title('Search Engine')
root.geometry("592x800")

myLabel = Label(root)


# Title of the GUI
title = Label(root, text='Query Searcher')
title.config(font=('helvetica', 30))
title.grid(row=0, column=0, pady=20)


def findURLs():
    stemTokens = open("stemmer.txt", 'r')
    stem_text = stemTokens.read()
    stems_dict = eval(stem_text)
    stemTokens.close()

    docID = open("docID.txt", 'r')  # {URL: docID}
    docID_text = docID.read()
    docID_dict = eval(docID_text)  # Dictionary {URL: docID}

    URLs = []

    beginTimer = time.time()  # Start Query Time
    lsts = docID_dict.values()
    result = set(lsts[0]).intersection(*lsts)
    URLs.append(result)
    for token, docID in docID_dict.items():
        stem = stems_dict[token]
        docIDs = docID_dict[stem]
        url = docID_dict[docIDs]
        URLs.append(url)
    stopTimer = time.time()
    totalTime = stopTimer - beginTimer
    return URLs, totalTime


# Respond to Enter/button click
def onClick(event=None):
    global myLabel
    myLabel.destroy()  # clear previous output

    queries = e.get()
    if len(queries) == 0:  # ignore empty input
        return

    urls = ""
    example_dict, totalTime = findURLs()
    if queries in example_dict:
        result_len = str(len(example_dict[queries]))  # number of URLs
        for url in example_dict[queries]:
            urls += "\n\n" + url
        myLabel = Label(root, text=urls)

        # display time and number of results
        data = Label(root, text="{0} results ({1} seconds)".format(result_len, totalTime), fg="gray",
                     font=('helvetica', 20))
        data.grid(row=3, column=0, pady=10)
    else:
        myLabel = Label(root, text="Try searching a different query!")
    myLabel.config(font=('helvetica', 25))

    e.delete(0, 'end')  # clear the searchbar
    myLabel.grid(row=4, column=0)


# Search bar
e = Entry(root, width=40, font=('Helvetica', 25))
e.grid(row=1, column=0, padx=10, pady=10)

# Button
root.bind('<Return>', onClick)  # when Enter is pressed
myButton = Button(root, text="Search", command=onClick)
myButton.grid(row=2, column=0, pady=10)
myButton.config(font=('helvetica', 20), padx=10, pady=8)

root.mainloop()