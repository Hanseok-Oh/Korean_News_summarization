import pandas as pd
from konlpy.tag import Hannanum
import re

def read_data(filename, encoding='utf-8'):
    # stop_word_list.txt를 부르기 위해서 사용
    # text 파일을 한줄씩 \n(줄바꿈)을 기준으로 읽는다.
    with open(filename, 'r', encoding=encoding) as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        return data

class Processing:
    def __init__(self):
        self.hannanum = Hannanum()
        self.stop_words = read_data(filename='sub_data/korean_stopwords_list.txt')

    def read_file(self,filename):
        # data 구조 : 날짜, 언론사, 제목, 본문, 링크
        df = pd.read_excel(filename, index_col=0)
        return df

    def cleanText(self,sentence):
        # 특수문자를 제거 (.을 제외)
        assert type(sentence) == str
        cleaned_sentence = re.sub('[^\w. ]', '', sentence)
        return cleaned_sentence

    def extract_nouns(self,sentence):
        assert type(sentence) == str
        return self.hannanum.nouns(sentence)

    def remove_stopword(self,tokened_sentence):
        # 미리 불러온 stop_words 리스트 안에 있는 단어일 경우 제거
        stopped_sentence = []
        stopwords = sum(self.stop_words,[])
        for word in tokened_sentence:
            if word in stopwords:
                continue
            stopped_sentence.append(word)
        return stopped_sentence


    def main(self,filename):
        '''
        :param sentences: txt 형식의 뉴스 기사
        :return: 전처리가 완료된 이중 리스트 형태의 단어들
        '''
        df = self.read_file(filename)
        print("preprocess -input file length:",len(df))
        sentences = df.iloc[:, 3]
        preprocessed_sentences = []

        for sentence in sentences:
            if type(sentence)!=str:
                continue

            temp = self.cleanText(sentence)
            # print("temp:",temp)
            temp1 = self.extract_nouns(temp)
            # print("temp1:", temp1)
            temp2 = self.remove_stopword(temp1)
            # print("temp2:", temp)
            preprocessed_sentences.append(temp2)

        return preprocessed_sentences
