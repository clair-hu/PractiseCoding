# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:13:34 2019

@author: clair
"""

import sys

from BlockCommentFileCommentsDesc import *
from BlockCommentDiffSingleCommentFileCommentsDesc import *
from BlockCommentSameSingleCommentFileCommentsDesc import *
from SingleCommentFileCommentsDesc import *
from CommentTypeConfig import *
from Exceptions import *


def getFileType(fileName):
    try:
        if (fileName.split("/")[-1].find(".") == 0):
            raise HiddenFileError(fileName)
        if (fileName.split("/")[-1].find(".") == -1):
            raise NoExtentionError(fileName)
        extention = fileName.split(".")[-1]
        return extention
    except HiddenFileError as e:
        print(e.message)
    except NoExtentionError as e:
        print(e.message)
        

def getFileCommentsDesc(fileName):
    fileType = getFileType(fileName)
    # TODO based on extention, map delimiters
    if fileType in BlockCommentDiffSingleCommentType:
        return BlockCommentDiffSingleCommentFileCommentsDesc(fileName, "/*", "*/", "//")
    elif fileType in BlockCommentSameSingleCommentType:
        return BlockCommentSameSingleCommentFileCommentsDesc(fileName, "'''", "#")
    elif fileType in SingleCommentType:
        return SingleCommentFileCommentsDesc(fileName, "#")
    elif fileType in BlockCommentType:
        return BlockCommentFileCommentsDesc(fileName, "<!--", "-->")
    
    

# main
fileName = str(sys.argv[1])
commentsDesc = getFileCommentsDesc(fileName)
print("Total # of lines: " + str(commentsDesc.getNumberOfLines()))
print("Total # of comment lines: " + str(commentsDesc.getNumberOfCommentsLines()))
print("Total # of single line comments: " + str(commentsDesc.getNumberOfSingleLineCommentsLines()))
print("Total # of comment lines within block comments: " + str(commentsDesc.getNumberOfBlockLineCommentsLines()))
print("Total # of block line comments: " + str(commentsDesc.getNumberOfBlockLineComments()))
print("Total # of TODO’s: " + str(commentsDesc.getNumberOfTODOes()))
