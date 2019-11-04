import argparse
import warnings
warnings.filterwarnings('ignore')

from models.dataCrawl import Crawling
from models.preprocess import Processing
from models.LDA import ModelLDA
from models.extractive_summarizer import Summarizer

# argparse

def define_argparser():
    parser = argparse.ArgumentParser(description = 'main argparser')
    parser.add_argument('--max_page',required=False,default=30,help= 'crawling을 실시할 페이지 수')
    parser.add_argument('--query',required=True, help='crawling을 실시할 검색어 명')
    parser.add_argument('--s_date',required=False, default='2019.01.01',help='crawling을 실시할 시작 날짜')
    parser.add_argument('--e_date',required=False, default='2019.03.31',help='crawling을 실시할 끝 날짜')
    parser.add_argument('--result_path',required=False, default='C:/Users/rnfek/hanseok/Korean_News_summarization/',help='crawling을 완성한 파일을 저장할 위치')
    # parser.add_argument('--file_name', required=True, help='요약을 진행할 txt파일명을 입력하시오.')
    parser.add_argument('--index', required=False, default=0, type=int, help='요약을 진행할 txt파일의 index를 입력하시오.')
    parser.add_argument('--number', required=False, default=2, type=int, help='결과로 제시할 문장 수를 입력하시오.')

    args = parser.parse_args()
    return args

def main(args):
    # crawler
    c= Crawling(args.max_page, args.query, args.s_date, args.e_date,args.result_path)
    c.main()
    p = Processing()
    documents = p.main(args.result_path+'data/{}_contents_text.txt'.format(args.query))
    print("LDA processing...")
    m = ModelLDA(documents)
    m.main()

    f = open(args.result_path + "data/{}_lda.txt".format(args.query), 'w',encoding='utf-8')
    f.close()
    for i,topic in enumerate(m.document_topic_counts):
        f = open(args.result_path + "data/{}_lda.txt".format(args.query), 'a',encoding='utf-8')
        # print("{}번째 본 article: ".format(i), documents[i][:10])
        data = "{}번째 본 article: {}\n".format(i,documents[i][:10])
        f.write(data)
        # print("{}번째 주제 배정 결과".format(i),topic)
        data = "{}번째 주제 배정 결과: {}\n".format(i,topic)
        f.write(data)
        for key in topic.keys():
            print("{}번째 key:".format(i),key)
            data ="{}번째 key: {}\n".format(i,key)
            f.write(data)
            print(m.topic_word_counts[key])
            # data= "{}번째 word: {}\n\n".format(i,m.topic_word_counts[key])
            # f.write(data)
            f.close()
            break

    s = Summarizer()
    s.main(args)
    return


'''
다음 process
query -> 문서별 주제/ 단어/주제별 단어 -> (주제를 직관화 시키는 과정 필요) -> 주제별로 하나의 문서를 선택 -> 요약 작업 실시
선택된 주제별로 하나의 문서를 고른다고 가정할 때, return 값

'''


if __name__ =='__main__':
    args = define_argparser()
    main(args)

