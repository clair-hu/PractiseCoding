# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:20:24 2019

@author: clair
"""

class BlockComment:
    def __init__(self):
        self.lines = []
        
    def addLine(self, line):
        self.lines.append(line)
        
    def getNumberOfLines(self):
        return len(self.lines)