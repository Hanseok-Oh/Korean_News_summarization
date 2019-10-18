import pandas as pd
import konlpy
from konlpy.tag import Hannanum
import re

def read_data(filename, encoding='utf-8'):
    # stop_word_list.txt를 부르기 위해서 사용
    # text 파일을 한줄씩 \n(줄바꿈)을 기준으로 읽는다.
    with open(filename, 'r', encoding=encoding) as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        return data

class processing:
    def __init__(self):
        self.hannanum = Hannanum()
        self.stop_words = read_data(filename='korean_stopwords_list.txt')

    def read_file(self,filename):
        # data 구조 : 날짜, 언론사, 제목, 본문, 링크
        df = pd.read_csv(filename, sep='\t', names=['date', 'company', 'title', 'body', 'link'])
        return df

    def cleanText(self,sentence):
        # 특수문자를 제거
        cleaned_sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\’\\‘|\(\)\[\]\<\>`\'…》ⓒ▶]', '', sentence)
        return cleaned_sentence

    def extract_nouns(self,sentence):
        assert type(sentence) == str
        return self.hannanum.nouns(sentence)

    def remove_stopword(self,tokened_sentence):
        # 미리 불러온 stop_words 리스트 안에 있는 단어일 경우 제거
        stopped_sentence = []
        for word in tokened_sentence:
            if word in self.stop_words:
                continue
            stopped_sentence.append(word)
        return stopped_sentence


    def main(self,filename):
        '''
        :param sentences: 뉴txt 형식의 뉴스 기사
        :return: 전처리가 완료된 이중 리스트 형태의 단어들
        '''
        df = self.read_file(filename)
        sentences = df.iloc[:, 3]
        preprocessed_senteces = []
        for sentence in sentences:
            temp = self.cleanText(sentence)
            temp1 = self.extract_nouns(temp)
            temp2 = self.remove_stopword(temp1)
            preprocessed_senteces.append(temp2)

        return preprocessed_senteces

# 전처리 프로세스 : input sentence -> lemmatization-> 정규표현식으로 특수문자 제거 / stopword제거 -> 사용할 품사만 추출
# 현재 : input sentence -> 특수문자 제거 -> 명사추출 -> 불용어 제거

#
# p = processing()
# print(p.main('data/두산모빌리티_contents_text.txt'))