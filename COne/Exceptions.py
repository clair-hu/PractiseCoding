# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:26:23 2019

@author: clair
"""

class HiddenFileError(Exception):
    def __init__(self, fileName):
        self.fileName = fileName
        self.message = "'" + self.fileName + "' is a hidden file, pass."
        
class NoExtentionError(Exception):
    def __init__(self, fileName):
        self.fileName = fileName
        self.message = "'" + self.fileName + "' file has no extention, invalid file type."
