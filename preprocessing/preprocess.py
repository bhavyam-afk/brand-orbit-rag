# lowercase, puntuation, tokenise to perform, stemming, stop words
import string
from utils.utils import load_stopwords
from nltk.stem import PorterStemmer

def lowercase(text):
    return text.lower()

def puntuate(text):
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def tokenise(text):
    tokens = []
    # tokens
    words = text.split()
    for word in words:
        if word:
            tokens.append(word)
    
    # stop words detection
    stopWords = load_stopwords()
    goodTokens =[]
    for token in tokens:
        if token not in stopWords:
            goodTokens.append(token)

    # stem the meanings
    stemmer = PorterStemmer()
    final_tokens = []
    for token in goodTokens:
        final_tokens.append(stemmer.stem(token))

    return final_tokens


def preprocess(text):
    text = lowercase(text)
    text = puntuate(text)
    tokens = tokenise(text)
    return tokens

