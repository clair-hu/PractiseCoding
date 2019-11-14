# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 16:08:21 2019

@author: clair
"""

from FileCommentsDesc import *
from BlockComment import *
import re

class BlockCommentSameSingleCommentFileCommentsDesc(FileCommentsDesc):
    def __init__(self, fileName, blockDelimiter, singleAndBlockDelimiter):
        super().__init__(fileName)

        self.blockDelimiter = blockDelimiter
        self.singleAndBlockDelimiter = singleAndBlockDelimiter
        self.readFileAndCloseFile()
    
    def readFileAndCloseFile(self):
        f = open(self.fileName, "r")
        
        tempBlockComment = BlockComment()
        blockCommentHasStarted = False
        singleAndBlockCommentHasStarted = False
        
        for line in f:
            self.numLines += 1
            inCommentRange = 0
            if self.isDelimiterValidInLine(self.blockDelimiter, line) == True or blockCommentHasStarted == True:
                inCommentRange = 0
#                 0 => line is not comment
#                 1 => single line comment
#                 2 => first line of block comment
#                 3 => middle line of block comment
#                 4 => last line of block comment
                if blockCommentHasStarted == False:
#                 first line of block comment
                    self.numCommentsLines += 1
                    inCommentRange = 2
                    blockCommentHasStarted = True
                    tempBlockComment.addLine(line)
                else:
                    if self.isDelimiterValidInLine(self.blockDelimiter, line) == True:
#                         last line of block comment
                        self.numCommentsLines += 1
                        inCommentRange = 4
                        blockCommentHasStarted = False
                        tempBlockComment.addLine(line)
                        self.blockComments.append(tempBlockComment)
                        tempBlockComment = BlockComment()
                    else:
#                         middle line of block comment
                        self.numCommentsLines += 1
                        inCommentRange = 3
                        tempBlockComment.addLine(line)
                self.checkTODOesInBlockComment(inCommentRange, line)
            else:
                inCommentRange = 0
#                 0 => line is not comment
#                 1 => line is a comment
                if singleAndBlockCommentHasStarted == True and self.isPotentialBlockCommentLine(self.singleAndBlockDelimiter, line) == True:
                    self.numCommentsLines += 1
                    if tempBlockComment.getNumberOfLines() == 0:
                        firstLine = self.singleLineComments.pop()
                        tempBlockComment.addLine(firstLine)
                    inCommentRange = 1
                    tempBlockComment.addLine(line)
                else:
                    if self.isDelimiterValidInLine(self.singleAndBlockDelimiter, line) == True:
                        singleAndBlockCommentHasStarted = self.isPotentialBlockCommentLine(self.singleAndBlockDelimiter, line)
                        self.numCommentsLines += 1
                        inCommentRange = 1
                        self.singleLineComments.append(line)
                    else:
                        if tempBlockComment.getNumberOfLines() > 0:
                            self.blockComments.append(tempBlockComment)
                            tempBlockComment = BlockComment()
                        singleAndBlockCommentHasStarted = False

                self.checkTODOesInSingleAndBlockComment(inCommentRange, line)
 
        f.close()
    
    def isPotentialBlockCommentLine(self, delimiter, line):
        return super().isDelimiterValidInLine(delimiter, line) and line.lstrip().find(delimiter) == 0
    
    def checkTODOesInBlockComment(self, inCommentRange, line):
        if inCommentRange == 0:
            return
        p = re.compile("todo", re.IGNORECASE)
        delimiterIndex = line.find(self.blockDelimiter)
        todoes = p.findall(line)
        todoIndex = 0
        for t in todoes:
            todoIndex = line.find(t, todoIndex + 1)
            if inCommentRange == 3:
                self.TODOes.append(line[todoIndex:])
            elif inCommentRange == 4:
                if todoIndex < delimiterIndex:
                    self.TODOes.append(line[todoIndex:])
            elif inCommentRange == 2:
                if todoIndex > delimiterIndex:
                    self.TODOes.append(line[todoIndex:])

    
    def checkTODOesInSingleAndBlockComment(self, inCommentRange, line):
        if inCommentRange == 0:
            return
        else:
            p = re.compile("todo", re.IGNORECASE)
            delimiterIndex = line.find(self.singleAndBlockDelimiter)
            todoes = p.findall(line)
            todoIndex = 0
            for t in todoes:
                todoIndex = line.find(t, todoIndex + 1)
                if todoIndex > delimiterIndex:
                    self.TODOes.append(line[todoIndex:])