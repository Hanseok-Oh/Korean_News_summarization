from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import re
import pandas as pd
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
        data = pd.read_excel(file_name)
        content_data = data.loc[:, 'contents']
        filedata = content_data[index] # indexing으로 원하는 기사 접근 가능

        temp = filedata

        for i in range(0, len(temp)//3):
            if temp[i:i + 3] == '기자]' or temp[i:i + 3] == '자 =' or temp[i:i + 3] == ' 기자':
                temp = temp[i + 3:]
                break

        sentence =temp
        # temp= re.sub('[-=+,#/\?:^$*\"※~&%ㆍ!』\’\‘|\(\)\[\]\<\>`\'…》ⓒ▶▲↑↓◆△]', '', sentence)
        temp = re.sub('[^\w. ]', '', sentence) #숫자,문자 그리고 .을 제외한 모든 특수문자 제거

        article = [sentence+'다' for sentence in temp.split('다.')]

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

        result = round(1 - cosine_distance(vector1, vector2),5)
        # print("type:",type(result))
        if not(result>=0):
            return 0
        else:
            return result
        # return round(1 - cosine_distance(vector1, vector2),5)


    def build_similarity_matrix(self, sentences, stopwords):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:  # ignore if both are same sentences
                    continue
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2], stopwords)

        return similarity_matrix


    def generate_summary(self,file_name,top_n,index):
        stopwords = read_data(filename='korean_stopwords_list.txt')
        stopwords = sum(stopwords,[])
        summarize_text = []

        # Step 1 - Read text anc split it
        sentences = self.read_article(file_name,index)

        #token화 추가
        hannanum = Hannanum()
        temp = []
        for sentence in sentences:
            temp.append(hannanum.nouns(' '.join(sentence)))

        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = self.build_similarity_matrix(temp, stopwords)
        # Step 3 - Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        # 12/2 edit.
        is_okay= True
        max_iter =500
        while is_okay:
            try:
                scores = nx.pagerank(sentence_similarity_graph,max_iter=max_iter)
                is_okay = False
            except:
                print("max_iter + 100:",max_iter)
                max_iter+=100

        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        # 11/29 수정
        summarize_text.append(' '.join(sentences[0]))
        for i in range(top_n):
            if len(ranked_sentence) <= i:
                break

            if ranked_sentence[i][1]==sentences[0]:
                print("\nalready first sentence is in summarize result")
                continue
            summarize_text.append(" ".join(ranked_sentence[i][1]))

        # Step 5 - Offcourse, output the summarize text
        print("\nSummarize Text of index-{}: \n".format(index), ". ".join(summarize_text))
        return ". ".join(summarize_text)

    def main(self,args):
        return self.generate_summary(args.result_path+'/data/{}/crawling.xlsx'.format(args.query),args.number,args.index)

    def mainForWeb(self,file_name,index,number):
        return self.generate_summary(file_name,index, number)

