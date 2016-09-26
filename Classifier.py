class Classifier :


    def __init__(self,trainingSet, testSet, dataClass, trainedClassifier):
        self.trainingSet = trainingSet
        self.testSet = testSet
        self.dataClass = dataClass
        self.trainedClassifier = trainedClassifier


    def setTrainingSet(self,trainingSet):
        self.trainingSet = trainingSet

    def getTrainingSet(self):
        return self.trainingSet

    def setTestSet(self,testSet):
        self.testSet = testSet

    def getTestSet(self):
        return self.testSet

    def getDataClass(self):
        return self.dataClass

    def setDataClass (self,dataClass):
        self.dataClass = dataClass

    def getTrainedClassifier(self):
        return self.trainedClassifier

    def setTrainedClassifier(self,trainedClassifier):
        self.trainedClassifier = trainedClassifier




    def __repr__(self):
        return "Training Set : " + str(self.trainingSet) + "/nTestSet : " + str(self.testSet)



