import argparse
import warnings
warnings.filterwarnings('ignore')

from models.dataCrawl import crawling
from models.preprocess import processing
from models.LDA import modelLDA

# argparse
parser = argparse.ArgumentParser(description = 'main argparser')
parser.add_argument('--max_page',required=False,default=10,help= 'crawling을 실시할 페이지 수')
parser.add_argument('--query',required=True, help='crawling을 실시할 검색어 명')
parser.add_argument('--s_date',required=False, default='2019.01.01',help='crawling을 실시할 시작 날짜')
parser.add_argument('--e_date',required=False, default='2019.03.31',help='crawling을 실시할 끝 날짜')
parser.add_argument('--result_path',required=False, default='C:/Users/rnfek/hanseok/Korean_News_summarization/',help='crawling을 완성한 파일을 저장할 위치')
# parser.add_argument('--file_name',required=True,help = '요약을 진행할 txt파일명을 입력하시오.')

args = parser.parse_args()


def main(args):
    # crawler
    crawling(args.max_page, args.query, args.s_date, args.e_date,args.result_path)
    p = processing()
    documents = p.main(args.result_path+'data/{}_contents_text.txt'.format(args.query))
    m = modelLDA(documents)
    m.main()

    for i,topic in enumerate(m.document_topic_counts):
        print("{}번째 본 article: ".format(i), documents[i][:10])
        print("{}번째 주제 배정 결과".format(i),topic)
        for key in topic.keys():
            print("{}번째 key:".format(i),key)
            print(m.topic_word_counts[key])
            break

    return

if __name__ =='__main__':
    main(args)

