import nltk
import re
# from sets import Set

class SentenceGrammarAnalyzer:
    REPLY_POS_VALID_UNIVERSAL_TAGS = set(['CONJ'])
    # check http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html for
    # a good list
    REPLY_POS_VALID_UPENN_TAGS = set(['WDT', 'DT'])
    REPLY_STARTERS = set(['ok', 'ok.', 'k', 'k.' 'mine', 'his', 'hers', 'theirs', 'ours'])

    def __init__(self, message, tokenizer):
        self.message = message
        self.tokenizer = tokenizer

    def isAReply(self):
        stemmedTokens = self.tokenizer.stemAndTokenize(self.message)
        text = self.message.getText()

        if len(stemmedTokens) <= 1:
            return (True, 'stemmed length of ' + str(len(stemmedTokens)))

        tokens = self.tokenizer.tokenize(self.message)
        univeralTags = nltk.pos_tag(tokens, tagset='universal')

        if univeralTags[0][1] in SentenceGrammarAnalyzer.REPLY_POS_VALID_UNIVERSAL_TAGS:
            return (True, 'universal tag ' + univeralTags[0][1])

        upennTags = nltk.pos_tag(tokens)
        if upennTags[0][1] in SentenceGrammarAnalyzer.REPLY_POS_VALID_UPENN_TAGS:
            return (True, 'upenn tag ' + upennTags[0][1])
        if tokens[0].lower() in SentenceGrammarAnalyzer.REPLY_STARTERS:
            return (True, 'reply starter ' + tokens[0].lower())
        if re.search('<@(\S*)>', text):
            return (True, 'reply text to a user id ' + re.findall('<@(\S*)>', text)[0])
        return (False, 'not a reply')
