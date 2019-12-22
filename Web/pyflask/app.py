from flask import Flask,render_template,url_for,request, redirect
import sys
import os
sys.path.insert(0,os.getcwd().replace("\\",'/'))
from web_main import main
import easydict

app = Flask(__name__)

query = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show', methods = ['GET','POST'])
def show():
    if request.method =='POST':
        global query
        query = request.form['query']
        s_date = "2019.01.01" #시작지점 편리화를 위한 지정
        e_date = request.form['e_date']
        args = easydict.EasyDict({"query": query, "s_date": s_date, "e_date": e_date})
        topic_keywords, summarized_text = main(args)

        topic_keywords1=topic_keywords[0]
        topic_keywords2 = topic_keywords[1]
        topic_keywords3 = topic_keywords[2]

        summarized_text1 = sum(summarized_text[:2], [])
        summarized_text1 = " ".join(summarized_text1)

        summarized_text2 = sum(summarized_text[2:4], [])
        summarized_text2 = " ".join(summarized_text2)

        summarized_text3 = sum(summarized_text[4:6], [])
        summarized_text3 = " ".join(summarized_text3)


    return render_template('show.html', query = query,topic_keywords1 = topic_keywords1,summary1 = summarized_text1, \
                           topic_keywords2=topic_keywords2, summary2=summarized_text2,\
                           topic_keywords3=topic_keywords3, summary3=summarized_text3)


@app.route('/LDA_Visualization',methods = ['GET','POST'])

def lda_visualzation():
    return render_template('LDA_Visualization/{}.html'.format(query))


@app.route('/summary')
def summary():
    return render_template('summary.html')



if __name__=='__main__':
    app.run(debug=True)


