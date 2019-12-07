# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:22:40 2019

@author: clair
"""

from FileCommentsDesc import *
from BlockComment import *
import re

class BlockCommentDiffSingleCommentFileCommentsDesc(FileCommentsDesc):
    def __init__(self, fileName, beginDelimiterBlock, endDelimiterBlock, endOfLineDelimiter):
        super().__init__(fileName)

        self.beginDelimiterBlock = beginDelimiterBlock
        self.endDelimiterBlock = endDelimiterBlock
        self.endOfLineDelimiter = endOfLineDelimiter
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
#             5 => line of block comment
            if blockCommentHasStarted == True and self.isDelimiterValidInLine(self.endDelimiterBlock, line) == False:
                self.numCommentsLines += 1
                inCommentRange = 3
                tempBlockComment.addLine(line)
            if self.isDelimiterValidInLine(self.endOfLineDelimiter, line) == True:
                self.numCommentsLines += 1
                inCommentRange = 1
                self.singleLineComments.append(line)
            elif self.isDelimiterValidInLine(self.beginDelimiterBlock, line) == True:
                if self.isDelimiterValidInLine(self.endDelimiterBlock, line) == True\
                and blockCommentHasStarted == False:
#                     line of block comment
                    self.numCommentsLines += 1
                    inCommentRange = 5
                    tempBlockComment.addLine(line)
                    self.blockComments.append(tempBlockComment)
                    tempBlockComment = BlockComment()
                else:
#                     first line of block comment
                    self.numCommentsLines += 1
                    inCommentRange = 2
                    blockCommentHasStarted = True
                    tempBlockComment.addLine(line)
            elif self.isDelimiterValidInLine(self.endDelimiterBlock, line) == True:
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
        todoes = p.findall(line)
        todoIndex = 0
        for t in todoes:
            todoIndex = line.find(t, todoIndex + 1)
            if inCommentRange == 3:
                self.TODOes.append(line[todoIndex:])
            elif inCommentRange == 4:
                delimiterIndex = line.find(self.endDelimiterBlock)
                if todoIndex < delimiterIndex:
                    self.TODOes.append(line[todoIndex:])
            elif inCommentRange == 2:
                delimiterIndex = line.find(self.beginDelimiterBlock)
                if todoIndex > delimiterIndex:
                    self.TODOes.append(line[todoIndex:])
            elif inCommentRange == 1:
                delimiterIndex = line.find(self.endOfLineDelimiter)
                if todoIndex > delimiterIndex:
                    self.TODOes.append(line[todoIndex:])
            elif inCommentRange == 5:
                beginDelimiterIndex = line.find(self.beginDelimiterBlock)
                endDelimiterIndex = line.find(self.endDelimiterBlock)
                if todoIndex > beginDelimiterIndex and todoIndex < endDelimiterIndex:
                    self.TODOes.append(line[todoIndex:])
                    
                    
commentsDesc = BlockCommentDiffSingleCommentFileCommentsDesc("data/PlaneFuelTest.java", "/*", "*/", "//")
#commentsDesc = getFileCommentsDesc(fileName)
print("Total # of lines: " + str(commentsDesc.getNumberOfLines()))
print("Total # of comment lines: " + str(commentsDesc.getNumberOfCommentsLines()))
print("Total # of single line comments: " + str(commentsDesc.getNumberOfSingleLineCommentsLines()))
print("Total # of comment lines within block comments: " + str(commentsDesc.getNumberOfBlockLineCommentsLines()))
print("Total # of block line comments: " + str(commentsDesc.getNumberOfBlockLineComments()))
print("Total # of TODO’s: " + str(commentsDesc.getNumberOfTODOes()))