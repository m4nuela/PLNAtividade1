import nltk
from Document import Document
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
# files = files[:100]

# ACQ 2369 != 1829
# TRADE 488 != 485
# CORN  237 != 238

# print(len(reuters.fileids('acq')))

trainingSet = []
testSet = []

for file in files:
    preprocessedFile = preprocessFile(file)

    index = file.find('training')
    if (index != -1):
        trainingSet.append(preprocessedFile)
    else:
        index = file.find('test')
        if (index != -1):
            testSet.append(preprocessedFile)

print('----Training Set----')
print(len(trainingSet))
# print(trainingSet)

print('\n')
print('----Test Set----')
print(len(testSet))
# print(testSet)


training = [[makeDictionary(x.getContent()), x.getCategory()] for x in trainingSet]
testing = [[makeDictionary(x.getContent()), x.getCategory()] for x in testSet]

## naive bayes
classifier = nltk.NaiveBayesClassifier.train(training)
print nltk.classify.accuracy(classifier, testing)