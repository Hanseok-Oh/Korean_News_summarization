import nltk
from nltk.corpus import stopwords
import numpy as np
import re
import pandas as pd

from gensim.summarization.summarizer import summarize


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
        # article = filedata.split(".")
        article= filedata
        print("article: ",article)

        return article


    def generate_summary(self,file_name, index,top_n=5):
        stop_words = read_data(filename='korean_stopwords_list.txt')

        summarize_text = []

        # Step 1 - Read text anc split it
        sentences = self.read_article(file_name,index)
        print("summary: ",summarize(sentences))

    def main(self,a,b,c):
        self.generate_summary('data/crawling_{}.xlsx'.format(a),b, c)

s =Summarizer()
s.main('현대자동차',1,2)