class QuestionSplitter:
    def __init__(self, fileName):
        self.splitNodeList = self.__split__(fileName)
        
    def __split__(self, fileName) -> list:
        with open(fileName, "r") as file:
            fullLines = file.readlines()

        thisSplitNodeList = list()

        i = 0
        ansStrs = list()
        splitNode = list()
        cnt = 1
        while i <= len(fullLines):
            if i == len(fullLines):
                line = fullLines[i-1]
            else:
                line = fullLines[i]
            
            if line == "\n" and cnt == 1:
                cnt += 1
                i += 1
                continue
            elif line == "\n" or i == len(fullLines):
                answerText = "".join(ansStrs)
                splitNode.append(answerText)
                thisSplitNodeList.append(tuple(splitNode))
                ansStrs = list()
                splitNode = list()
                cnt = 0
            elif "question" in line.lower():
                splitNode.append(line)
            elif cnt > 2:
                ansStrs.append(line)
            else:
                splitNode.append(line)
            cnt += 1
            i += 1
        
        return thisSplitNodeList

    def __print__(self):
        for node in self.splitNodeList:
            print("---NEW NODE---")
            
            print("OPEN: ", node[0])
            print("QUESTION: ", node[1])
            print("ANSWERS: ", node[2])

            print("---END NODE---")
            print("\n")
