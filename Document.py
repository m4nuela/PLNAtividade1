class Document :


    def __init__(self,fileID, category):
        self.fileID = fileID
        self.category = category
        self.content = []

    def setContent(self,content):
        self.content = content

    def getContent(self):
        return self.content

    def setFileID(self, fileID):
        self.fileID = fileID

    def getFileID(self):
        return self.fileID

    def setCategory(self, category):
        self.category = category

    def getCategory(self):
        return self.category


    def __repr__(self):
        return "FileID : " + self.fileID + "\nCategory : " + str(self.category) + "\nContent" + str(self.content)
