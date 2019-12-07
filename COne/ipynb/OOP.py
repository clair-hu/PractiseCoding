#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re


# In[2]:


class HiddenFileError(Exception):
    def __init__(self, fileName):
        self.fileName = fileName
        self.message = "'" + self.fileName + "' is a hidden file, pass."
        
class NoExtentionError(Exception):
    def __init__(self, fileName):
        self.fileName = fileName
        self.message = "'" + self.fileName + "' file has no extention, invalid file type."


# In[3]:


def getFileType(fileName):
    try:
        if (fileName.find(".") == 0):
            raise HiddenFileError(fileName)
        if (fileName.find(".") == -1):
            raise NoExtentionError(fileName)
        extention = fileName.split(".")[-1]
        return extention
    except HiddenFileError as e:
        print(e.message)
    except NoExtentionError as e:
        print(e.message)


# In[9]:


BlockCommentDiffSingleCommentType = ["java", "cpp", "c"]
SingleCommentType = ["py"]
BlockCommentType = ["xml", "html"]
def getFileCommentsDesc(fileName):
    fileType = getFileType(fileName)
    if fileType in BlockCommentDiffSingleCommentType:
        return BlockCommentDiffSingleCommentFileCommentsDesc(fileName, "/*", "*/", "//")
    elif fileType in SingleCommentType:
        return SingleCommentFileCommentsDesc(fileName, "#")
    elif fileType in BlockCommentType:
        return BlockCommentFileCommentsDesc(fileName, "<!--", "-->")


# In[5]:


class BlockComment:
    def __init__(self):
        self.lines = []
        
    def addLine(self, line):
        self.lines.append(line)
        
    def getNumberOfLines(self):
        return len(self.lines)


# In[20]:


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
#     def addValidTODOes()
#     def checkTODOes()
#     def readFileAndCloseFile()
    


# In[13]:


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
            if self.isDelimiterValidInLine(self.beginDelimiter, line) == True                and self.isDelimiterValidInLine(self.endDelimiter, line) == True:
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
        elif inCommentRange == 1:
            self.addValidTODOes(self.beginDelimiter + self.endDelimiter, line)
        elif inCommentRange == 2:
            self.addValidTODOes(self.beginDelimiter, line)
        elif inCommentRange == 3:
            self.addValidTODOes("", line)
        elif inCommentRange == 4:
            self.addValidTODOes(self.endDelimiter, line)
            
    def addValidTODOes(self, delimiter, line):
        p = re.compile("todo", re.IGNORECASE)
        beginDelimiterIndex = line.find(self.beginDelimiter)
        endDelimiterIndex = line.find(self.endDelimiter)
        todoes = p.findall(line)
        todoIndex = 0
        for t in todoes:
            todoIndex = line.find(t, todoIndex)
            if delimiter == "":
                self.TODOes.append(line[todoIndex:])
            elif delimiter == self.endDelimiter:
                if todoIndex < endDelimiterIndex:
                    self.TODOes.append(line[todoIndex:])
            elif delimiter == self.beginDelimiter:
                if todoIndex > beginDelimiterIndex:
                    self.TODOes.append(line[todoIndex:])
            else:
                if todoIndex > beginDelimiterIndex and todoIndex < endDelimiterIndex:
                    self.TODOes.append(line[todoIndex:])


# In[14]:


bbf = getFileCommentsDesc("agents.xml")


# In[15]:


bbf.getNumberOfLines()


# In[16]:


bbf.getNumberOfBlockLineComments()


# In[17]:


bbf.getNumberOfBlockLineCommentsLines()


# In[18]:


bbf.getNumberOfTODOes()


# In[19]:


bbf.getNumberOfCommentsLines()


# In[20]:


class BlockCommentDiffSingleCommentFileCommentsDesc(FileCommentsDesc):
    def __init__(self, fileName, beginDelimiterBlock, endDelimiterBlock, endOfLineDelimiter):
        super().__init__(fileName)

        self.beginDelimiterBlock = beginDelimiterBlock
        self.endDelimiterBlock = endDelimiterBlock
        self.endOfLineDelimiter = endOfLineDelimiter
        self.readFileAndCloseFile()
  
    def addValidTODOes(self, delimiter, line):
        p = re.compile("todo", re.IGNORECASE)
        delimiterIndex = line.find(delimiter)
        todoes = p.findall(line)
        todoIndex = 0
        for t in todoes:
            todoIndex = line.find(t, todoIndex)
            if delimiter == "":
                self.TODOes.append(line[todoIndex:])
            elif delimiter == self.endDelimiterBlock:
                if todoIndex < delimiterIndex:
                    self.TODOes.append(line[todoIndex:])
            else:
                if todoIndex > delimiterIndex:
                    self.TODOes.append(line[todoIndex:])
                
    def checkTODOes(self, inCommentRange, line):
        if inCommentRange == 0:
            return
        elif inCommentRange == 1:
            self.addValidTODOes(self.endOfLineDelimiter, line)
        elif inCommentRange == 2:
            self.addValidTODOes(self.beginDelimiterBlock, line)
        elif inCommentRange == 3:
            self.addValidTODOes("", line)
        elif inCommentRange == 4:
            self.addValidTODOes(self.endDelimiterBlock, line)
    
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
            if blockCommentHasStarted == True and self.isDelimiterValidInLine(self.endDelimiterBlock, line) == False:
                self.numCommentsLines += 1
                inCommentRange = 3
                tempBlockComment.addLine(line)
            if self.isDelimiterValidInLine(self.endOfLineDelimiter, line) == True:
                self.numCommentsLines += 1
                inCommentRange = 1
                self.singleLineComments.append(line)
            elif self.isDelimiterValidInLine(self.beginDelimiterBlock, line) == True:
#                 TODO assume no nested block comments
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


# In[12]:


bf = BlockCommentDiffSingleCommentFileCommentsDesc("PlaneFuelTest.java", "/*", "*/", "//")


# In[13]:


bf.getNumberOfLines()


# In[14]:


bf.getNumberOfBlockLineComments()


# In[15]:


bf.getNumberOfBlockLineCommentsLines()


# In[16]:


bf.getNumberOfCommentsLines()


# In[17]:


bf.getNumberOfSingleLineCommentsLines()


# In[18]:


bf.getNumberOfTODOes()


# In[27]:


class SingleCommentFileCommentsDesc(FileCommentsDesc):
    def __init__(self, fileName, delimiter):
        super().__init__(fileName)

        self.delimiter = delimiter
        self.readFileAndCloseFile()
    
    def isPotentialBlockCommentLine(self, delimiter, line):
        return super().isDelimiterValidInLine(delimiter, line) and line.lstrip().find(delimiter) == 0
    
    def addValidTODOes(self, line):
        p = re.compile("todo", re.IGNORECASE)
        delimiterIndex = line.find(self.delimiter)
        todoes = p.findall(line)
        todoIndex = 0
        for t in todoes:
            todoIndex = line.find(t, todoIndex)
            if todoIndex > delimiterIndex:
                self.TODOes.append(line[todoIndex:])
                
    def checkTODOes(self, inCommentRange, line):
        if inCommentRange == 0:
            return
        else:
            self.addValidTODOes(line)
    
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


# In[23]:


sf = SingleCommentFileCommentsDesc("python.py", "#")


# In[21]:


sf.getNumberOfLines()


# In[22]:


sf.getNumberOfBlockLineComments()


# In[23]:


sf.getNumberOfBlockLineCommentsLines()


# In[25]:


sf.getNumberOfCommentsLines()


# In[30]:


sf.getNumberOfSingleLineCommentsLines()


# In[31]:


sf.getNumberOfTODOes()


# In[ ]:





# In[ ]:




