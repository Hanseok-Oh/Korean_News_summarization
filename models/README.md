
## 0. models
code flow : dataCrawl -> preprocess -> LDA -> summarization

### 0.1 dataCrawl.py
------------------
[bumcrush 님의 기본 코드 구조](https://bumcrush.tistory.com/116)를 참조하여 적용했습니다. 


<pre><code> 
class Crawling:
    def __init__(self, max_page, query, s_date, e_date, result_path):
        self.result_path = result_path + '/data'
        self.max_page = max_page
        self.query = query
        self.s_date = s_date
        self.e_date = e_date
        print("crawling: ", self.query)
        
    ...
    
    def excel_make(self, query, date):
        data = pd.read_csv(self.result_path + '/{}_contents_text.txt'.format(query), sep='\t', header=None,
                           error_bad_lines=False)
        data.columns = ['years', 'company', 'title', 'contents', 'link']
        xlsx_outputFileName = '{}.xlsx'.format(query)
        data.to_excel(self.result_path + '/crawling_' + xlsx_outputFileName, encoding='utf-8')
        return

</code></pre>
    
    

=> years, company(언론사), title, contents, link 의 column에 맞춰서 

RESULT_PATH+'/{}_contents_text.txt'.format(query) 형태로 파일이 저장됨 

같은 내용으로 excel 파일 {query}.xlsx

### 0.2 preprocess.py 
----------------
input sentence -> 특수문자 제거 -> 명사추출 -> 불용어 제거

<pre><code>
def main(self,filename):
    '''
    :param sentences: txt 형식의 뉴스 기사
    :return: 전처리가 완료된 이중 리스트 형태의 단어들
    '''
    df = self.read_file(filename)
    sentences = df.iloc[:, 3]
    preprocessed_senteces = []
    for sentence in sentences:
        if type(sentence)!=str:
            continue
        temp = self.cleanText(sentence)
        temp1 = self.extract_nouns(temp)
        temp2 = self.remove_stopword(temp1)
        preprocessed_senteces.append(temp2)

    return preprocessed_senteces
</pre></code>

- How to use
  processing.main(filename) 형식으로 사용 

  filename은 앞선 datacrawl.py 에서 형성된 txt 형태의 파일 형식을 따름
  
  본문의 기사 내용만을 다루기에 indexing을 해주고 
  
  return 값으로 명사만 추출되고, 불용어가 제거된 기사별 문장이 분리된 이중 리스트 형태의 단어들을 돌려줌



### 0.3 LDA.py (in progress) 
--------------
[ratsgo 블로그 참조](https://ratsgo.github.io/from%20frequency%20to%20semantics/2017/07/09/lda/)

하이퍼파라미터 K를 설정하여 몇 개의 토픽을 추출할 것인지 결정
document에 존재하는 단어들이 어떤 topic에 속할 확률이 가장 높은지 계산하여, document 별로 가장 높은 확률의 topic을 찾음
각 토픽별 단어 비중을 확인하여 어떠한 특성을 지닌 주제인지 파악 가능 

- To do
> 각 토픽을 대표하는 문서를 추출하는 방법을 찾아야 함
> 각 토픽에서 단어들을 보고 이슈(주제)를 명명할 근거를 찾아야 함


### 0.4 extractive_summarizer.py 
--------------------------
[edubey/text_summarizer](https://github.com/edubey/text-summarizer)의 깃헙을 참고하여 수정하였습니다. 

뉴스 기사 하나의 본문에 대한 내용을 원하는 수의 문장으로 요약

해당 스크립트 하나만 실행하면 요약 결과 제시

자세한 내용을 알고 싶으신 분들은 [본 깃헙내 설명글](https://github.com/Hanseok-Oh/Text_Summarization/tree/master/%5B10%5Dcode/edubey_text_summarizer)을 참조해주세요.

