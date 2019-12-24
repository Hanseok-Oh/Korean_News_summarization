import argparse
from multiprocessing import Pool
import warnings
import os
warnings.filterwarnings('ignore')
import shutil
import time
from tqdm import tqdm
import pandas as pd

from models.crawl import Crawling
from models.preprocess import Processing
from models.lda import LDA
from models.extractive_summarizer import Summarizer

import pyLDAvis.gensim


def main(args):

    print("query is :", args.query)
    result_path = os.getcwd().replace("\\",'/')

    new_directory = result_path + '/data/{}'.format(args.query)

    reset_mode =False

    if reset_mode:
        if os.path.exists(new_directory):
            shutil.rmtree(new_directory)
            time.sleep(1)


    if not os.path.exists(new_directory):
        print("Making new directory \n")
        os.mkdir(new_directory)
        c = Crawling(args.query, args.s_date, args.e_date, result_path)
        # page 수 조정 가능
        for i in tqdm(range(1, 301, 10)):
            c.main(page=i)
        #new
        p = Processing()
        documents = p.main(result_path + '/data/{}/crawling.xlsx'.format(args.query))

        print("LDA processing...")
        a = LDA(documents)
        ldamodel, vis = a.selected_model()

        pyLDAvis.save_html(vis, result_path + '/data/{}/LDA_Visualization.html'.format(args.query))
        pyLDAvis.save_html(vis, result_path + '/Web/pyflask/templates/LDA_visualization/{}.html'.format(args.query))
        print("Visualization of LDA result is saved in directory.")

        a.format_topics_sentences(ldamodel, args.query).to_excel(new_directory+'/lda.xlsx'.format(args.query))
        a.extract_index_per_topic(ldamodel, args.query).to_excel(
            result_path + '/data/{}/lda_best.xlsx'.format(args.query))

        target_index = a.extract_index_per_topic(ldamodel, args.query).index
        print("target_index:",target_index)

        s = Summarizer()
        f = open(new_directory+'/summary.txt'.format(args.query), 'w', encoding='utf-8')
        for i, index in enumerate(target_index):
            try:
                f.write("Summarize Text of topic - {}, index-{}: \n".format(topic + 1, index))
                f.write(s.generate_summary(new_directory+'/crawling.xlsx'.format(args.query), args.number,index)+'\n')
                f.write("link: " + pd.read_excel(new_directory+'/crawling.xlsx'.format(args.query)).loc[index, 'link'] + "\n\n")
            except:
                continue
        f.close()


    lda_best = pd.read_excel(new_directory + '/lda_best.xlsx')
    topic_keywords = []
    for keys in lda_best['Keywords']:
        topic_keywords.append([keys])

    summarize_result = []
    f = open(new_directory + '/summary.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        summarize_result.append([line])
    f.close()

    return topic_keywords,summarize_result
