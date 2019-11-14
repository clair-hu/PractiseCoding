# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:10:32 2019

@author: clair
"""

import re

class FileCommentsDesc:
    def __init__(self, fileName):
        self.fileName = fileName
        self.blockComments = []
        self.singleLineComments = []
        self.TODOes = []
        self.numCommentsLines = 0
        self.numLines = 0
        
    def getNumberOfLines(self):
        return self.numLines
    
    def getNumberOfCommentsLines(self):
        return self.numCommentsLines
    
    def getNumberOfSingleLineCommentsLines(self):
        return len(self.singleLineComments)
    
    def getNumberOfBlockLineCommentsLines(self):
        return self.getNumberOfCommentsLines() - self.getNumberOfSingleLineCommentsLines()
    
    def getNumberOfBlockLineComments(self):
        return len(self.blockComments)
    
    def getNumberOfTODOes(self):
        return len(self.TODOes)
    
    def setNumberOfLines(self, num):
        self.numLines = num
    
#     check whether delimiter in "", using regex
    def isDelimiterValidInLine(self, delimiter, line):
        p = r'"([^"]*)"'
        removeQuotesText = re.sub(p, "", line)
        return delimiter in removeQuotesText
    
# #     virtual methods to be implemented by child classes
#     def readFileAndCloseFile()
#     def checkTODOes()    
