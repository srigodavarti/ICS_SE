token_to_docID_dict = {}

if __name__ == "__main__":
    finalIndex = open("finalIndex.txt", 'r')
    index_text = finalIndex.read()
    index_dict = eval(index_text)
    finalIndex.close()

    for token, lst in index_dict.items():
        doc_id_lst = []
        for tpl in lst:
            doc_id_lst.append(tpl[2])
        token_to_docID_dict[token] = doc_id_lst

    token_docID_file = open("tokenDocID.txt", 'a+', encoding="utf-8")
    token_docID_file.write(str(token_to_docID_dict))
    token_docID_file.close()

