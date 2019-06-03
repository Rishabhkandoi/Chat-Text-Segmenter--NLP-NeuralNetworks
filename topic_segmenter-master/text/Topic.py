import gensim
from gensim.corpora import Dictionary
from nltk import FreqDist
from nltk import word_tokenize
from nltk.collocations import BigramCollocationFinder
from sklearn.feature_extraction.text import CountVectorizer
import comparison


class Topic:
    def __init__(self, startMessage, reason):
        self.startMessage = startMessage
        self.messages = [startMessage]
        self.reasons = [reason]

    def appendMessage(self, message, reason):
        self.messages.append(message)
        self.reasons.append(reason)

    def getMessages(self):
        return self.messages

    def getReasons(self):
        return self.reasons

    def getStartMessage(self):
        return self.startMessage

    def size(self):
        return len(self.messages)

    def absorve(self, other):
        self.messages = self.messages + other.messages
        self.messages.sort(key=lambda x: x.getID())
        self.reasons.extend( other.reasons )  # append reasons from other topic

    def nameTheTopic(self, message, tokenizer):
        message = self.concatenate_list_data(message, tokenizer)
        finder = BigramCollocationFinder.from_words(word_tokenize(message))
        f = finder.ngram_fd.items()
        flipped = list([(v, k) for k, v in f])
        flipped.sort(reverse=True)
        if float(flipped[0][0]) > 1:
            s = " "
            return s.join(flipped[0][1]).title()
        else:
            frequency = FreqDist(word_tokenize(message))
            return frequency.most_common(1)[0][0].title()

    def concatenate_list_data(self, list, tokenizer):
        result = []
        sep = " "
        for element in list:
            result.append(sep.join(tokenizer.stemAndTokenize(element)))
        return str(sep.join(result))

    def saveBagOfWords(self, message, tokenizer, i):
        messageNew = self.concatenate_list_data(message, tokenizer)
        # frequency = FreqDist(word_tokenize(messageNew))
        # s = "BagofWords/" + i + ".txt"
        # dictlist = []
        # for key, value in frequency.items():
        #     temp = [key, value]
        #     dictlist.append(temp)
        # print(dictlist)
        # f = open(s, "w+")
        # f.write(str(dictlist))
        # dictionary = Dictionary(word_tokenize(messageNew))
        # corpus = [dictionary.doc2bow(text) for text in word_tokenize(messageNew)]
        # print(corpus)
        comparison.comparison([word_tokenize(messageNew)])
