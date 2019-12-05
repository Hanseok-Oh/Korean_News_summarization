from flask import Flask,render_template,url_for,request, redirect
import sys
import os
# print("here!:",os.getcwd())
sys.path.insert(0,os.getcwd().replace("\\",'/'))
from web_main import main
import easydict

app = Flask(__name__)

@app.route('/')
def index():
    # if request.method =='POST':
    #     query = request.form['query']
    #     s_date = request.form['s_date']
    #     e_date = request.form['e_date']
    #     args = easydict.EasyDict({"query": query, "s_date": s_date, "e_date": e_date})
    #     summarized_text = main(args)
    #     print("\nsummarized_text:",summarized_text)
    #     summarized_text = '아따 요약좀 됐으면 합니다.'
    #     value_list = ['query','summarized_text']
    #     return redirect(url_for('/summary'))
    return render_template('index.html')

@app.route('/show', methods = ['GET','POST'])
def show():
    # query = '삼성전자'
    # return 'Summarized text for %s is ' % query
    if request.method =='POST':
        ## for real test
        # query = request.form['query']
        # s_date = request.form['s_date']
        # e_date = request.form['e_date']
        # number = 3
        # args = easydict.EasyDict({"query": query, "s_date": s_date, "e_date": e_date,'number':number})
        # target_index, summarized_text = main(args)

        ## for temp test
        temp_query = '삼성전자'
        temp_target_index ='5, 7, 10, 12'
        temp_summary = '삼성전자는 앞으로 한석이를 채용하기로 했다 샷'
        temp_summary2 = '또 뭐를 넣을테야'

    # return render_template('show.html', query = query,target_index = target_index)
    return render_template('show.html', query = temp_query,target_index = temp_target_index,summary = temp_summary,summary2 = temp_summary2)

@app.route('/summary')
def summary():
    if request.method =='POST':
    return render_template('summary.html')

@app.route('/lda')
def summary():
    if request.method =='POST':
    return render_template('lda.html')


if __name__=='__main__':
    app.run(debug=True)


