import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import re
import pandas as pd
import argparse
from konlpy.tag import Hannanum


def read_data(filename, encoding='utf-8'):
    # stop_word_list.txt를 부르기 위해서 사용
    # text 파일을 한줄씩 \n(줄바꿈)을 기준으로 읽는다.
    with open(filename, 'r', encoding=encoding) as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        return data

class Summarizer:
    def __init__(self):
        pass

    def read_article(self,file_name,index):
        # method2
        # target = '삼성생명'
        data = pd.read_excel(file_name)
        content_data = data.loc[:, 'contents']
        filedata = content_data[index] # indexing으로 원하는 기사 접근 가능

        temp = filedata
        print("\n\norigin :",temp)
        if ']' in temp[:len(temp) // 2]:
            temp = temp.split(']')[1:]  # 기사 앞 [기자이름] 부분 제거
            temp = ' '.join(temp)

        if '@' in temp:
            temp = temp.split('@')[:-1]  # 기사 앞 [기자이름] 부분 제거
            temp = ' '.join(temp)

        if '.' in temp:
            temp = temp.split('.')[:-1]
            temp = '. '.join(temp)
            sentence = temp

        temp= re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\’\\‘|\(\)\[\]\<\>`\'…》ⓒ▶]', '', sentence)
        article = temp.split('.')

        # print("\nthe end:",article)
        result =[]
        for sentence in article:
            temp=[]
            for token in sentence.split():
                if token!='':
                    temp.append(token)
            result.append(temp)

        # print("\nresult: ",result)
        return result


    def sentence_similarity(self,sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords = []

        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]

        all_words = list(set(sent1 + sent2))

        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

        # build the vector for the first sentence
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1

        # build the vector for the second sentence
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1


        return 1 - cosine_distance(vector1, vector2)


    def build_similarity_matrix(self,sentences, stop_words):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:  # ignore if both are same sentences
                    continue
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

        return similarity_matrix


    def generate_summary(self,file_name, index,top_n=5):
        stop_words = read_data(filename='korean_stopwords_list.txt')

        summarize_text = []

        # Step 1 - Read text anc split it
        sentences = self.read_article(file_name,index)

        #token화 추가
        hannanum = Hannanum()
        temp = []
        for sentence in sentences:
            temp.append(hannanum.nouns(' '.join(sentence)))
        # print("temp:",temp)

        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = self.build_similarity_matrix(temp, stop_words)

        # Step 3 - Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        for i in range(top_n):
            summarize_text.append(" ".join(ranked_sentence[i][1]))

        # Step 5 - Offcourse, output the summarize text
        print("\nSummarize Text: \n", ". ".join(summarize_text))
        return ". ".join(summarize_text)

    # def main(self,args):
    #     return self.generate_summary(args.result_path+'/data/crawling_{}.xlsx'.format(args.query),args.index, args.number)
    def main2(self,file_name,index,number):
        return self.generate_summary(file_name,index, number)


# 길이에 대한 normalize
# 벡터화 시 TFIDF 기반으로 가중치를 준다.