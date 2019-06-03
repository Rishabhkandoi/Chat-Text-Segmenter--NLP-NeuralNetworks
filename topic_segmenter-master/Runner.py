import sys

from text.Message import Message
from grammar.MessageTokenizer import MessageTokenizer
from segmenter.ConversationSegmenter import ConversationSegmenter
from text.JSONParser import JSONParser
import comparison

class TestRunner:
    def __init__(self, json_file_name):
        self.jsonFileName = json_file_name

    def run(self):
        parser = JSONParser(self.jsonFileName)
        self.messages = parser.getMessages()
        self.tokenizer = MessageTokenizer()
        windowSize = 3
        cosineSimilarityThreshold = 0.8
        segmenter = ConversationSegmenter(
            self.messages, windowSize, cosineSimilarityThreshold, self.tokenizer)
        topics = segmenter.segment()
        self.report(topics)

    def report(self, topics):
        idGroups = []
        bag = []
        previous_topic = ""
        print("============================= detailed ========================")
        for topic in topics:
            current_topic = topic.nameTheTopic(topic.getMessages(), self.tokenizer)
            if previous_topic != current_topic:
                print("\n")
                print("== Topic ==")
                idGroup = []
            else:
                print("\n\t------Following topic has same topic name as the previous one")
            for (message, reason) in zip(topic.getMessages(), topic.getReasons()):
                idGroup.append(message.getID())
                print("\n\t------ id: \t" + str(message.getID()) + "\t" + reason)
                print("" + message.getText())
            if previous_topic != current_topic:
                idGroups.append(idGroup)
                previous_topic = current_topic


        print("===============================")

        print("============================= short ========================")
        previous_topic = ""
        i = 1
        for topic in topics:
            current_topic = topic.nameTheTopic(topic.getMessages(), self.tokenizer)
            if previous_topic != current_topic:
                print("\n")
                print("== Topic: " + current_topic + "  ==")
                previous_topic = current_topic
            for message in topic.getMessages():
                print(str(message.getID()) + ":\t" + message.getText())
            topic.saveBagOfWords(topic.getMessages(), self.tokenizer, str(i))
            i = i+1

        print(idGroups)
        # comparison.comparison(bag)


def main(json_input):
    TestRunner(json_input).run()

if __name__ == '__main__':
    main("sample/data.json")
