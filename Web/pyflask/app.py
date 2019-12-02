from flask import Flask,render_template,url_for,request, redirect
import sys
import os
print("here!:",os.getcwd())
sys.path.insert(0, "C:/Users/rnfek/hanseok/Korean_News_summarization")
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

@app.route('/summarize', methods = ['GET','POST'])
def view():
    # query = '삼성전자'
    # return 'Summarized text for %s is ' % query
    if request.method =='POST':
        query = request.form['query']
        s_date = request.form['s_date']
        e_date = request.form['e_date']
        args = easydict.EasyDict({"query": query, "s_date": s_date, "e_date": e_date})
        summarized_text = main(args)
        print("\nsummarized_text:",summarized_text)
        # summarized_text = '아따 요약좀 됐으면 합니다.'
        # value_list = ['query', 'summarized_text']
    return render_template('summary.html', query = query)



if __name__=='__main__':
    app.run(debug=True)


