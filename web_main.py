import argparse
from multiprocessing import Pool
import warnings
import os
warnings.filterwarnings('ignore')
import shutil
import time
from tqdm import tqdm

from models.crawl import Crawling
from models.preprocess import Processing
from models.lda import LDA
from models.extractive_summarizer import Summarizer

import pyLDAvis.gensim


def main(args):
    # s_date='2019.01.01'
    # e_date='2019.03.31'

    print("query is :", args.query)
    # os.chdir('../../')
    print("getcwd in web_main: ", os.getcwd())
    result_path = os.getcwd().replace("\\",'/')

    new_directory = result_path + '/data/{}'.format(args.query)

    # if os.path.exists(new_directory):
    #     shutil.rmtree(new_directory)
    #     time.sleep(1)
    #     os.mkdir(new_directory)

    # if not os.path.exists(new_directory):
    #     os.mkdir(new_directory)

    if not os.path.exists(new_directory):
        os.mkdir(new_directory)
        c = Crawling(args.query, args.s_date, args.e_date, result_path)
        # page 수 조정 가능
        for i in tqdm(range(1, 71, 10)):
            c.main(page=i)

    p = Processing()
    documents = p.main(result_path + '/data/{}/crawling.xlsx'.format(args.query))

    print("LDA processing...")
    a = LDA(documents)
    ldamodel,vis = a.selected_model()

    # pyLDAvis.save_html(vis, result_path + '/data/{}/LDA_Visualization.html'.format(args.query))
    print("Visualization of LDA result is saved in directory.")

    a.format_topics_sentences(ldamodel,args.query).to_excel(result_path+'/data/{}/lda.xlsx'.format(args.query))
    a.extract_index_per_topic(ldamodel,args.query).to_excel(result_path + '/data/{}/lda_best.xlsx'.format(args.query))

    target_index = a.extract_index_per_topic(ldamodel,args.query).index
    print("target index:", target_index)

    s = Summarizer()
    summarize_result = []

    f= open(result_path+'/data/{}/summary.txt'.format(args.query),'a',encoding='utf-8')
    for i,index in enumerate(target_index):
        f.write("Summarize Text of topic-{},index-{}: \n".format(i+1,index))
        f.write(s.generate_summary(result_path+'/data/{}/crawling.xlsx'.format(args.query),args.number,index) + '\n')

        summarize_result.append(["Summarize Text of topic-{},index-{}: \n".format(i+1,index)\
        + s.generate_summary(result_path+'/data/{}/crawling.xlsx'.format(args.query),args.number,index) + '\n'])

    f.close()

    return target_index,summarize_result
