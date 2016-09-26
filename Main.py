import nltk
from Document import Document
from Classifier import Classifier
from nltk.corpus import reuters
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
import re

import random

categories = ['earn', 'acq', 'money-fx', 'grain', 'crude', 'trade', 'interest', 'ship', 'wheat', 'corn']

porterStemmer = PorterStemmer()
stopSet = set(stopwords.words('english'))
punctuations = set(string.punctuation)
stopAndPuctuationSet = stopSet | punctuations


# print(stopAndPuctuationSet)

def checkNotANumber(word):
    obj = re.match(r'[a-z][a-z]+', word, re.I)
    if obj:
        if obj.group() == word:
            return True
    return False


def findCategory(clist):
    c = [0] * len(categories)
    for i in range(0, len(c)):
        if categories[i] in clist:
            c[i] += 1
    return c


classifierIndex = {
        'earn':0,
        'acq':1,
        'money-fx':2,
        'grain':3,
        'crude':4,
        'trade':5,
        'interest':6,
        'ship':7,
        'wheat':8,
        'corn':9
    }



def preprocessFile(file):
    tokens = nltk.word_tokenize(' '.join(reuters.words(file)))

    # # we should be using this one
    #category = findCategory(reuters.categories(file))


    # # but for now we can test with this
    category = [x for x in reuters.categories(file) if x in categories][0]



    document = Document(file, category)
    content = []
    for token in tokens:
        if token not in stopAndPuctuationSet and checkNotANumber(token):
            stemmedWord = porterStemmer.stem(token.lower())
            content.append(stemmedWord)

    document.setContent(content)
    return document


def makeDictionary(array):
    return dict([[x, "True"] for x in array])


# print(reuters.fileids())
# print(reuters.categories())


files = reuters.fileids(categories)
#random.shuffle(files)
#files = files[:500]

# ACQ 2369 != 1829
# TRADE 488 != 485
# CORN  237 != 238

# print(len(reuters.fileids('acq')))

trainingSet = []
testSet = []
classifierPerCategory = []


# it goes from 0 to 9...
for i in range(0,10):
    category = categories[i]

    for file in files:
        preprocessedFile = preprocessFile(file)

        categoriesFile = [x for x in reuters.categories(file) if x in categories]

        if (category in categoriesFile):
            preprocessedFile.setCategory(1)
        else:
            preprocessedFile.setCategory(0)


        index = file.find('training')
        if (index != -1):
            trainingSet.append(preprocessedFile)
        else:
            index = file.find('test')
            if (index != -1):
                testSet.append(preprocessedFile)

    training = [[makeDictionary(x.getContent()), x.getCategory()] for x in trainingSet]
    testing = [[makeDictionary(x.getContent()), x.getCategory()] for x in testSet]

    trainedClassifier = nltk.NaiveBayesClassifier.train(training)
    classifier = Classifier(training, testing, category, trainedClassifier)
    classifierPerCategory.append(classifier)

print('----Training Set----')
print(len(trainingSet))
# print(trainingSet)

print('\n')
print('----Test Set----')
print(len(testSet))
# print(testSet)


print(len(classifierPerCategory))

#print(classifierPerCategory[0]);


print(type(list(reuters.categories(testSet[0].getFileID()))))


hits = 0
for file in testSet:
    fileCategories = [x for x in reuters.categories(file.getFileID()) if x in categories]
    found = False
    for category in fileCategories:
        index = int(classifierIndex.get(category))
        classifier = classifierPerCategory[index].getTrainedClassifier()
        # test_file = [makeDictionary(file.getContent()), file.getCategory()]
        test_file = makeDictionary(file.getContent())
        classification = nltk.NaiveBayesClassifier.classify(classifier, test_file)
        #print(classification)

        print
        print("Classifier : " + category)
        print("Classification : " + str(classification))
        print("Classes : " + str(reuters.categories(file.getFileID())))
        if (classification == 1):
            found=True

    if found == True:
        hits = hits + 1


print("HITS : " +str(hits))
print("TestSetLen : " + str(len(testSet)))
accuracy = float(float(hits)/float((len(testSet))))
print("Acuracia : " + str(accuracy))

        #print("Classificador Classe " + str(i) + " , " + categories[i])
        #classifier = nltk.NaiveBayesClassifier.train(classifierPerCategory[i].getTrainingSet())
        #print(nltk.NaiveBayesClassifier.classify(classifier,classifierPerCategory[i].getTestSet()))
        #print nltk.classify.accuracy(classifier, classifierPerCategory[i].getTestSet())



#training = [[makeDictionary(x.getContent()), x.getCategory()] for x in trainingSet]
#testing = [[makeDictionary(x.getContent()), x.getCategory()] for x in testSet]

## naive bayes
#classifier = nltk.NaiveBayesClassifier.train(training)
#print nltk.classify.accuracy(classifier, testing)