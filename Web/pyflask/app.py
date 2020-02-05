from flask import Flask,render_template,request
import sys
import os
sys.path.insert(0,os.getcwd().replace("\\",'/'))
from web_main import main
from trend import SearchTrend
from financialReport import MakeReport

import easydict

app = Flask(__name__)

query,s_date,e_date ='','','2020.02.05'
topic_keywords1,topic_keywords2,topic_keywords3,summarized_text1,summarized_text2,summarized_text3 = '','','','','',''
args ={}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show', methods = ['GET','POST'])
def show():
    if request.method =='POST':
        global query,s_date,e_date,args,topic_keywords1,topic_keywords2,topic_keywords3,summarized_text1,summarized_text2,summarized_text3
        query = request.form['query']
        s_date = "2019.09.01" #시작지점 편리화를 위한 지정
        e_date = request.form['e_date']
        number = 3
        args = easydict.EasyDict({"query": query, "s_date": s_date, "e_date": e_date,"number":number})
        topic_keywords, summarized_text = main(args)

        topic_keywords1 = topic_keywords[0]
        topic_keywords2 = topic_keywords[1]
        topic_keywords3 = topic_keywords[2]

        summarized_text1 = sum(summarized_text[1:2], [])
        summarized_text1 = "\n".join(summarized_text1)

        summarized_text2 = sum(summarized_text[5:6], [])
        summarized_text2 = "\n".join(summarized_text2)

        summarized_text3 = sum(summarized_text[9:10], [])
        summarized_text3 = "\n".join(summarized_text3)


    return render_template('show.html', query = query,topic_keywords1 = topic_keywords1,summary1 = summarized_text1, \
                           topic_keywords2=topic_keywords2, summary2=summarized_text2,\
                           topic_keywords3=topic_keywords3, summary3=summarized_text3)


@app.route('/LDA_Visualization',methods = ['GET','POST'])
def lda_visualzation():
    return render_template('LDA_Visualization/{}.html'.format(query))


@app.route('/Search_Trend')
def search_trend():
    st = SearchTrend(args)
    st.plotTrend()
    return render_template('search_trend.html',query =query)

@app.route('/Financial_Report')
def financial_report():
    mr = MakeReport(args)
    mr.make_plot()
    return render_template('financial_report.html',query =query)


if __name__=='__main__':
    app.run(debug=False)


