'''
ratsgo github에서 LDA 코드를 가져와서 뉴스 데이터셋에 적용
https://gist.github.com/ratsgo/c68296fa65420f6d2d970781f02f5420
'''
import random
from collections import Counter

class ModelLDA:
    def __init__(self,documents):
        self.seed = random.seed(0)
        self.K = 4
        self.documents = documents
        self.document_topics = [[random.randrange(self.K) for word in document]
                           for document in self.documents]
        self.document_topic_counts = [Counter() for _ in self.documents]
        self.topic_word_counts = [Counter() for _ in range(self.K)]
        self.topic_counts = [0 for _ in range(self.K)]
        self.document_lengths = [len(document) for document in self.documents]
        self.distinct_words = set(word for document in self.documents for word in document)
        self.V = len(self.distinct_words)
        self.D = len(self.documents)

    def p_topic_given_document(self,topic, d, alpha=0.1):
        return ((self.document_topic_counts[d][topic] + alpha) /
                (self.document_lengths[d] + self.K * alpha))

    def p_word_given_topic(self,word, topic, beta=0.1):
        return ((self.topic_word_counts[topic][word] + beta) /
                (self.topic_counts[topic] + self.V * beta))

    def topic_weight(self,d, word, k):
        return self.p_word_given_topic(word, k) * self.p_topic_given_document(k, d)

    def choose_new_topic(self,d, word):
        return self.sample_from([self.topic_weight(d, word, k) for k in range(self.K)])

    def sample_from(self,weights):
        total = sum(weights)
        rnd = total * random.random()
        for i, w in enumerate(weights):
            rnd -= w
            if rnd <= 0:
                return i

    def main(self):
        for d in range(self.D):
            for word, topic in zip(self.documents[d], self.document_topics[d]):
                self.document_topic_counts[d][topic] += 1
                self.topic_word_counts[topic][word] += 1
                self.topic_counts[topic] += 1

        for iter in range(1000):
            for d in range(self.D):
                for i, (word, topic) in enumerate(zip(self.documents[d],
                                                      self.document_topics[d])):
                    self.document_topic_counts[d][topic] -= 1
                    self.topic_word_counts[topic][word] -= 1
                    self.topic_counts[topic] -= 1
                    self.document_lengths[d] -= 1
                    new_topic = self.choose_new_topic(d, word)
                    self.document_topics[d][i] = new_topic
                    self.document_topic_counts[d][new_topic] += 1
                    self.topic_word_counts[new_topic][word] += 1
                    self.topic_counts[new_topic] += 1
                    self.document_lengths[d] += 1

