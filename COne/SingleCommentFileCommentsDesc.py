# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:24:01 2019

@author: clair
"""

from FileCommentsDesc import *
from BlockComment import *
import re

class SingleCommentFileCommentsDesc(FileCommentsDesc):
    def __init__(self, fileName, delimiter):
        super().__init__(fileName)

        self.delimiter = delimiter
        self.readFileAndCloseFile()
    
    def readFileAndCloseFile(self):
        f = open(self.fileName, "r")
        
        tempBlockComment = BlockComment()
        blockCommentHasStarted = False
        
        for line in f:
            self.numLines += 1
            inCommentRange = 0
#             0 => line is not comment
#             1 => line is a comment
            if blockCommentHasStarted == True and self.isPotentialBlockCommentLine(self.delimiter, line) == True:
                self.numCommentsLines += 1
                if tempBlockComment.getNumberOfLines() == 0:
                    firstLine = self.singleLineComments.pop()
                    tempBlockComment.addLine(firstLine)
                inCommentRange = 1
                tempBlockComment.addLine(line)
            else:
                if self.isDelimiterValidInLine(self.delimiter, line) == True:
                    blockCommentHasStarted = self.isPotentialBlockCommentLine(self.delimiter, line)
                    self.numCommentsLines += 1
                    inCommentRange = 1
                    self.singleLineComments.append(line)
                else:
                    if tempBlockComment.getNumberOfLines() > 0:
                        self.blockComments.append(tempBlockComment)
                        tempBlockComment = BlockComment()
                    blockCommentHasStarted = False

            self.checkTODOes(inCommentRange, line)
 
        f.close()
        
        
        
    def isPotentialBlockCommentLine(self, delimiter, line):
        return super().isDelimiterValidInLine(delimiter, line) and line.lstrip().find(delimiter) == 0
                
    def checkTODOes(self, inCommentRange, line):
        if inCommentRange == 0:
            return
        else:
            p = re.compile("todo", re.IGNORECASE)
            delimiterIndex = line.find(self.delimiter)
            todoes = p.findall(line)
            todoIndex = 0
            for t in todoes:
                todoIndex = line.find(t, todoIndex + 1)
                if todoIndex > delimiterIndex:
                    self.TODOes.append(line[todoIndex:])