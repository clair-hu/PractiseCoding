# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:11:07 2019

@author: clair
"""

from FileCommentsDesc import *
from BlockComment import *
import re

class BlockCommentFileCommentsDesc(FileCommentsDesc):
    def __init__(self, fileName, beginDelimiter, endDelimiter):
        super().__init__(fileName)
        
        self.beginDelimiter = beginDelimiter
        self.endDelimiter = endDelimiter
        self.readFileAndCloseFile()
        
    def readFileAndCloseFile(self):
        f = open(self.fileName, "r")
        
        tempBlockComment = BlockComment()
        blockCommentHasStarted = False
        
        for line in f:
            self.numLines += 1
            inCommentRange = 0
#             0 => line is not comment
#             1 => single line comment
#             2 => first line of block comment
#             3 => middle line of block comment
#             4 => last line of block comment
            if blockCommentHasStarted == True and self.isDelimiterValidInLine(self.endDelimiter, line) == False:
                self.numCommentsLines += 1
                inCommentRange = 3
                tempBlockComment.addLine(line)
            if self.isDelimiterValidInLine(self.beginDelimiter, line) == True\
            and self.isDelimiterValidInLine(self.endDelimiter, line) == True:
                self.numCommentsLines += 1
                inCommentRange = 1
                self.singleLineComments.append(line)
            elif self.isDelimiterValidInLine(self.beginDelimiter, line) == True:
#                 TODO assume no nested block comments
                self.numCommentsLines += 1
                inCommentRange = 2
                blockCommentHasStarted = True
                tempBlockComment.addLine(line)
            elif self.isDelimiterValidInLine(self.endDelimiter, line) == True:
                self.numCommentsLines += 1
                inCommentRange = 4
                blockCommentHasStarted = False
                tempBlockComment.addLine(line)
                self.blockComments.append(tempBlockComment)
                tempBlockComment = BlockComment()
            
            self.checkTODOes(inCommentRange, line)
 
        f.close()
    
    def checkTODOes(self, inCommentRange, line):
        if inCommentRange == 0:
            return
        p = re.compile("todo", re.IGNORECASE)
        beginDelimiterIndex = line.find(self.beginDelimiter)
        endDelimiterIndex = line.find(self.endDelimiter)
        todoes = p.findall(line)
        todoIndex = 0
        for t in todoes:
            todoIndex = line.find(t, todoIndex + 1)
            if inCommentRange == 3:
                self.TODOes.append(line[todoIndex:])
            elif inCommentRange == 4:
                if todoIndex < endDelimiterIndex:
                    self.TODOes.append(line[todoIndex:])
            elif inCommentRange == 2:
                if todoIndex > beginDelimiterIndex:
                    self.TODOes.append(line[todoIndex:])
            elif inCommentRange == 1:
                if todoIndex > beginDelimiterIndex and todoIndex < endDelimiterIndex:
                    self.TODOes.append(line[todoIndex:])