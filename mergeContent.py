with open('sortFileContent.txt', 'r') as myfile:
  data = myfile.read()
  dict = eval(data)
  mergeWeightedTokens = {}
  for token, lst in dict.items():
      mergeTuple = [0, 0, lst[0][2]]
      for tpl in lst:
          mergeTuple[0] += tpl[0] #Frequency
          mergeTuple[1] += 1 #Num of Documents
          mergeWeightedTokens[token] = mergeTuple

mergeWeightedContent = open('mergeFileContentF.txt', 'a+', encoding="utf-8")
mergeWeightedContent.write(str(mergeWeightedTokens))
mergeWeightedContent.close()
