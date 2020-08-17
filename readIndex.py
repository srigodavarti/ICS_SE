
with open('finalIndex.txt', 'r') as myfile:
  data = myfile.read()
  dict = eval(data)
  regularDict = {}
  weightedDict = {}
  for key, value in dict.items():
    for tuple in value:
      file_content = (0, 0, 0, "file content")
      weighted_content = (0, 0, 0, "weighted content")
      if tuple[3] == file_content[3]:
        if key in regularDict:
          regularDict[key].append(tuple)
        else:
          regularDict[key] = [tuple]
      else:
        if key in weightedDict:
          weightedDict[key].append(tuple)
        else:
          weightedDict[key] = [tuple]

regularFile = open('fileContent.txt', 'a+', encoding="utf-8")
weightedFile = open('weightedContent.txt', 'a+', encoding="utf-8")
regularFile.write(str(regularDict))
weightedFile.write(str(weightedDict))
regularFile.close()
weightedFile.close()