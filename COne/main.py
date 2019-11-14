# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:13:34 2019

@author: clair
"""

from BlockCommentFileCommentsDesc import *
from BlockCommentDiffSingleCommentFileCommentsDesc import *
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
    if fileType in BlockCommentDiffSingleCommentType:
        return BlockCommentDiffSingleCommentFileCommentsDesc(fileName, "/*", "*/", "//")
    elif fileType in SingleCommentType:
        return SingleCommentFileCommentsDesc(fileName, "#")
    elif fileType in BlockCommentType:
        return BlockCommentFileCommentsDesc(fileName, "<!--", "-->")
    
    

# main
commentsDesc = getFileCommentsDesc("data/agents.xml")
print(commentsDesc.getNumberOfLines())
print(commentsDesc.getNumberOfBlockLineComments())
print(commentsDesc.getNumberOfBlockLineCommentsLines())
print(commentsDesc.getNumberOfSingleLineCommentsLines())
print(commentsDesc.getNumberOfCommentsLines())
print(commentsDesc.getNumberOfTODOes())