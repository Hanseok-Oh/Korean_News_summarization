import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import re

def read_data(filename, encoding='utf-8'):
    # stop_word_list.txt를 부르기 위해서 사용
    # text 파일을 한줄씩 \n(줄바꿈)을 기준으로 읽는다.
    with open(filename, 'r', encoding=encoding) as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        return data

def read_article(file_name):
    file = open(file_name, "r", encoding='utf-8')
    filedata = file.readlines()
    article = filedata[0].split(".")
    sentences = []
    removed = []
    print("article: ", article)
    for sentence in article:
        hangul = re.compile('[^ㄱ-ㅣ 가-힣]+')  # 정교화 필요
        sentences.append(hangul.sub('', sentence).split(" "))
        removed.append(hangul.findall(sentence))  # 제거된 단어들 확인 필요 시 return에 추가

    return sentences


def sentence_similarity(sent1, sent2, stopwords=None):
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


def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=5):
    stop_words = read_data(filename='korean_stopwords_list.txt')

    summarize_text = []

    # Step 1 - Read text anc split it
    sentences = read_article(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    # print("\nIndexes of top ranked_sentence order are \n", ranked_sentence)

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize texr
    print("\nSummarize Text: \n", ". ".join(summarize_text))


# let's begin
import argparse

parser = argparse.ArgumentParser(description = '파일명 & 요약할 문장 수')
parser.add_argument('--file_name',required=True,help = '요약을 진행할 txt파일명을 입력하시오.')
parser.add_argument('--number',required=False,default=2, help='결과로 제시할 문장 수를 입력하시오.')

# 입력받은 인자값을 args에 저장
args = parser.parse_args()
print(args.file_name, args.number)
# article당 본문 기사 데이터는 'data/articles_content'폴더에 존재
generate_summary('data/articles_content/'+args.file_name, int(args.number))