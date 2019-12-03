import argparse
from multiprocessing import Pool
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import os
import time

from models.crawl import Crawling
from models.preprocess import Processing
from models.lda import LDA
import pyLDAvis.gensim
import shutil

from models.extractive_summarizer import Summarizer


def define_argparser():
    parser = argparse.ArgumentParser(description = 'main argparser')
    parser.add_argument('--query',required=True, help='crawling을 실시할 검색어 명')

    parser.add_argument('--s_date',required=False, default='2019.01.01',help='crawling을 실시할 시작 날짜')
    parser.add_argument('--e_date',required=False, default='2019.03.31',help='crawling을 실시할 끝 날짜')
    parser.add_argument('--result_path',required=False, default=os.getcwd().replace("\\","/"),help='crawling을 완성한 파일을 저장할 위치')

    parser.add_argument('--crawl_only', required=False, default='False', help='crawling만 실시.')
    parser.add_argument('--page', required=False, default=range(1, 1001, 10), type=str, metavar ='range', help='크롤링을 실시할 페이지 수를 입력하세요.')

    parser.add_argument('--LDA_only', required=False, default='False', help='LDA만 실시.')

    parser.add_argument('--summary_only', required=False, default='False', help='요약만 진행할 지 여부.')
    parser.add_argument('--index', required=False, default=0, type=int,metavar='N', help='요약을 진행할 txt파일의 index를 입력하시오.')
    parser.add_argument('--number', required=False, default=2, type=int,metavar='N', help='결과로 제시할 문장 수를 입력하시오.')

    args = parser.parse_args()
    return args

def main(args):
    p = Processing()
    documents = p.main(args.result_path+'/data/{}/crawling.xlsx'.format(args.query))
    print("After preprocess-input file length:",len(documents))

    a = LDA(documents)
    ldamodel,vis = a.selected_model()

    pyLDAvis.save_html(vis, args.result_path + '/data/{}/LDA_Visualization.html'.format(args.query))
    print("Visualization of LDA result is saved in directory.")

    a.format_topics_sentences(ldamodel,args.query).to_excel(args.result_path+'/data/{}/lda.xlsx'.format(args.query))
    a.extract_index_per_topic(ldamodel,args.query).to_excel(args.result_path + '/data/{}/lda_best.xlsx'.format(args.query))

    target_index = a.extract_index_per_topic(ldamodel,args.query).index
    print("target index:", target_index)

    s = Summarizer()
    f= open(args.result_path+'/data/{}/summary.txt'.format(args.query),'a',encoding='utf-8')
    for i,index in enumerate(target_index):
        f.write("Summarize Text of topic-{},index-{}: \n".format(i,index))
<<<<<<< HEAD
        f.write(s.generate_summary(args.result_path+'/data/{}/crawling.xlsx'.format(args.query),args.number,index)+'\n')
=======
        f.write(s.generate_summary(args.result_path+'/data/{}/crawling.xlsx'.format(args.query),args.number,index) + '\n')
>>>>>>> b77719c37590828565e6ed128234fab35f1be085
    f.close()
    return


'''
다음 process
query -> 문서별 주제/ 단어/주제별 단어 -> (주제를 직관화 시키는 과정 필요) -> 주제별로 하나의 문서를 선택 -> 요약 작업 실시
선택된 주제별로 하나의 문서를 고른다고 가정할 때, return 값

'''


if __name__ =='__main__':
    args = define_argparser()
    # summarize only
    if args.summary_only =='True':
        s = Summarizer()
        target_index = pd.read_excel(args.result_path+'/data/{}/lda_best.xlsx'.format(args.query),index_col=0).index
        print("target index:",target_index)
        f = open(args.result_path + '/data/{}/summary.txt'.format(args.query),'w', encoding='utf-8')
        for topic,index in enumerate(target_index):
            f.write("Summarize Text of topic - {}, index-{}: \n".format(topic+1,index))
            f.write(s.generate_summary(args.result_path+'/data/{}/crawling.xlsx'.format(args.query),args.number,index)+'\n\n')
        f.close()

    elif args.LDA_only =='True':
        main(args)

    else:
        # crawler
        new_directory =args.result_path+'/data/{}'.format(args.query)
        if os.path.exists(new_directory):
            shutil.rmtree(new_directory)
            time.sleep(1)
            os.mkdir(new_directory)

        if not os.path.exists(new_directory):
            os.mkdir(new_directory)

        c = Crawling(args.query, args.s_date, args.e_date, args.result_path)
        print("crawler multiprocessing...")
        pool = Pool(processes=8)  # 4개의 프로세스를 사용합니다.
        try:
            pool.map(c.main, args.page)
        except Exception as e:
            print(e)


        if args.crawl_only == 'True':
            exit(1)
        else:
            main(args)

