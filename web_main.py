import argparse
from multiprocessing import Pool
import warnings
import os
warnings.filterwarnings('ignore')
import easydict

from models.dataCrawl import Crawling
from models.preprocess import Processing
from models.LDA import ModelLDA
from models.extractive_summarizer import Summarizer

def main(args):
    # s_date='2019.01.01'
    # e_date='2019.03.31'

    print("query is :", args.query)
    os.chdir('../../')
    print("getcwd in main2: ", os.getcwd())
    result_path = os.getcwd()
    result_path = result_path.replace("\\",'/')

    c = Crawling(args.query, args.s_date, args.e_date, result_path)
    # page 수 조정 가능
    c.main(page=11)
    p = Processing()
    documents = p.main(result_path+'/data/{}_contents_text.txt'.format(args.query))
    print("LDA processing...")
    m = ModelLDA(documents)
    m.main()
    f = open(result_path + "/data/{}_lda.txt".format(args.query), 'w',encoding='utf-8')
    f.close()
    for i,topic in enumerate(m.document_topic_counts):
        f = open(result_path + "/data/{}_lda.txt".format(args.query), 'a',encoding='utf-8')
        # print("{}번째 본 article: ".format(i), documents[i][:10])
        data = "{}번째 본 article: {}\n".format(i,documents[i][:10])
        f.write(data)
        # print("{}번째 주제 배정 결과".format(i),topic)
        data = "{}번째 주제 배정 결과: {}\n".format(i,topic)
        f.write(data)

        key = topic.most_common(1)[0][0]
        print("{}번째 key:".format(i), key)
        data = "{}번째 key: {}\n".format(i, key)
        f.write(data)
        print(m.topic_word_counts[key].most_common(30))
        data= "{}번째 word: {}\n\n".format(i,m.topic_word_counts[key].most_common(30))
        f.write(data)
        f.close()


    s = Summarizer()
    file_name = result_path + '/data/crawling_{}.xlsx'.format(args.query)
    index =1
    number =2
    summarized_text = s.main2(file_name,index,number)
    return summarized_text


'''
다음 process
query -> 문서별 주제/ 단어/주제별 단어 -> (주제를 직관화 시키는 과정 필요) -> 주제별로 하나의 문서를 선택 -> 요약 작업 실시
선택된 주제별로 하나의 문서를 고른다고 가정할 때, return 값

'''
\