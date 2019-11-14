# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:25:24 2019

@author: clair
"""

BlockCommentDiffSingleCommentType = ["java", "cpp", "c"] 
# has different begin delimiter and end delimiter for block comment, has different single-line-delimiter / endOfLine delimiter

BlockCommentSameSingleCommentType = ["py"]
# has block delimiter (begin and end delimiter are the same), has different single-line-delimiter / endOfLine delimiter

SingleCommentType = ["sql", "sh"]
# all delimiter are the same, whether single line or block depends on the lines covered

BlockCommentType = ["xml", "html"]
# has different begin delimiter and end delimiter, whether single line or block depends on the lines covered