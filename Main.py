import nltk
from Document import Document
from nltk.corpus import reuters
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
import re


porterStemmer = PorterStemmer()
stopSet = set(stopwords.words('english'))
punctuations = set(string.punctuation)
stopAndPuctuationSet = stopSet | punctuations

print(stopAndPuctuationSet)

def checkNotANumber(word):
    obj = re.match(r'[a-z][a-z]+',word,re.I)
    if obj:
        if obj.group() == word:
            return True
    return False


def preprocessFile(file):


    tokens = nltk.word_tokenize(' '.join(reuters.words(file)))
    document = Document(file,reuters.categories(file))
    content = []
    for token in tokens:
        if token not in stopAndPuctuationSet and checkNotANumber(token):
            stemmedWord = porterStemmer.stem(token.lower())
            content.append(stemmedWord)

    document.setContent(content)
    return document

#print(reuters.fileids())
#print(reuters.categories())


files = reuters.fileids(['earn','acq','money-fx', 'grain','crude', 'trade', 'interest','ship','wheat', 'corn'])


#ACQ 2369 != 1829
#TRADE 488 != 485
#CORN  237 != 238

#print(len(reuters.fileids('acq')))

trainingSet = []
testSet = []

for file in files:
    #print(reuters.categories(file));
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
print(trainingSet)


print('\n')
print('----Test Set----')
print(len(testSet))
print(testSet)
