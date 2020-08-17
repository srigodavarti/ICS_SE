with open('fileContent.txt', 'r') as myfile:
  data = myfile.read()
  dict = eval(data)
  fileDict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1][0], reverse=True)}
  sortFileContent = open('sortFileContent.txt', 'a+', encoding="utf-8")
  sortFileContent.write(str(fileDict))
  sortFileContent.close()

with open('weightedContent.txt', 'r') as myfile:
  data = myfile.read()
  dict = eval(data)
  fileDict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1][0], reverse=True)}

sortWeightedContent = open('sortWeightedContent.txt', 'a+', encoding="utf-8")
sortWeightedContent.write(str(fileDict))
sortWeightedContent.close()

sortFileContent = open('sortFileContent.txt', 'a+', encoding="utf-8")
sortFileContent.write(str(fileDict))
sortFileContent.close()