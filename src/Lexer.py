# import re

class Lexer:
    def __init__(self, line):
        # self.tokenList = self.__tobinizer__(line)
        self.tokenList = self.__tokenize__(line)
        self.lineLen = len(self.tokenList)
        self.loc = 0

    # def __tobinizer__(self, line):
    #     return self.__tokenize__(line)

    def __tokenize__(self, line: str):
        thisTokenList = list()
        allBooks = {
            "amos", "matthew", "exodus", "1 samuel", "1 timothy", "1 corinthians",
            "zephaniah", "malachi", "revelation", "proverbs", "joel", "numbers",
            "luke", "deuteronomy", "song of solomon", "judges", "jude", "ecclesiastes",
            "colossians", "galatians", "1 thessalonians", "nehemiah", "micah", "2 thessalonians",
            "2 peter", "ezra", "2 kings", "ephesians", "job", "2 chronicles",
            "daniel", "philemon", "obadiah", "james", "ruth", "lamentations",
            "1 chronicles", "1 john", "philippians", "psalms", "john", "haggai",
            "nahum", "leviticus", "hosea", "isaiah", "genesis", "titus",
            "2 samuel", "jonah", "ezekiel", "joshua", "habakkuk", "hebrews",
            "1 kings", "2 john", "romans", "1 peter", "esther", "acts",
            "3 john", "2 timothy", "zechariah", "mark", "jeremiah", "2 corinthians"
        }

        start = 0
        end = 0
        while end < len(line):
            char = line[end]

            # Extraneous handler: if previous is also extraneous skip
            if char in ",.;:?!- " and line[end-1] in ",.;:?!- ":
                start = end + 1
            
            # Word handler: slice when delimiter reached
            elif char in ",.;:?!- ": 
                word = line[start:end].lower()
                if word in allBooks:
                    thisTokenList.append(("book", word))
                else:
                    thisTokenList.append(("word", word))
                start = end + 1
            
            # Number handler: convert to int
            elif char.isdigit() and line[end+1].isdigit():
                    thisTokenList.append(("int", int(line[start:end+2])))
                    start = end + 3
                    end += 2
            elif char.isdigit():
                thisTokenList.append(("int", int(line[start:end+1])))
                start = end + 2
                end += 1

            # Quoted string handler: slice whole quote
            elif char == "\"":
                cnt = end + 1
                while True:
                    if line[cnt] == "\"":
                        thisTokenList.append(("quote", line[start+1:cnt].lower()))
                        start = cnt + 1
                        end = cnt
                        break
                    cnt += 1

            end += 1
        
        return thisTokenList
    
    def getLoc(self):
        return self.loc
    
    def setLoc(self, newLoc):
        self.loc = newLoc
        return True
    
    def getToken(self):
        if self.lineLen < 1:
            raise IndexError("Lexer is empty")
        return self.tokenList[self.loc]
    
    def nextToken(self):
        self.loc += 1
        if self.loc >= self.lineLen or self.lineLen < 1:
            # raise IndexError("Lexer is empty or reached end of line")
            return ("none", "none")
        return self.tokenList[self.loc]
    