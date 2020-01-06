
## 0. models (version a)
code flow : crawl.py -> preprocess.py -> lda.py -> extractive_summarizer.py

### 0.1 crawl.py
------------------
[bumcrush 님의 기본 코드 구조](https://bumcrush.tistory.com/116)를 참조하여 적용했습니다. 


<pre><code> 
class Crawling:
    def __init__(self, query, s_date, e_date, result_path):
        self.result_path = result_path + '/data'
        self.query = query
        self.s_date = s_date
        self.e_date = e_date
        self.article_links=[]
        print("crawling: ", self.query)       
    ...
    
    def excel_make(self, query):
        data = pd.read_csv(self.result_path + '/{}/contents.txt'.format(query), sep='\t', header=None,
                           error_bad_lines=False)
        data.columns = ['years', 'company', 'title', 'contents', 'link']
        out_file = self.result_path + '/{}/'.format(query) + 'crawling.xlsx'
        data.to_excel(out_file, encoding='utf-8')
        return

</code></pre>
    
=> years, company(언론사), title, contents, link 의 column에 맞춰서 

result_path +'/{}/contents.txt'.format(query) 형태로 파일이 저장됨 

같은 내용으로 excel 파일 {query}/crawling.xlsx

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
        print("preprocess -input file length:",len(df))
        sentences = df.iloc[:, 3]
        preprocessed_sentences = []

        for sentence in sentences:
            if type(sentence)!=str:
                continue

            temp = self.cleanText(sentence)
            temp1 = self.extract_nouns(temp)
            temp2 = self.remove_stopword(temp1)
            preprocessed_sentences.append(temp2)

        return preprocessed_sentences
</pre></code>

- How to use

  processing.main(filename) 형식으로 사용 

  filename은 앞선 crawl.py 에서 형성된 txt 형태의 파일 형식을 따름
  
  본문의 기사 내용만을 다루기에 indexing을 해주고 
  
  return 값으로 명사만 추출되고, 불용어가 제거된 기사별 문장이 분리된 이중 리스트 형태의 단어들을 돌려줌



### 0.3 lda.py  
--------------

<pre><code>
class LDA:
    def __init__(self, processed_data, passes=30, limit=12, start=3, step=2):
        self.texts = processed_data
        self.passes = passes
        self.dictionary = corpora.Dictionary(processed_data)
        self.corpus = [self.dictionary.doc2bow(text) for text in processed_data]

        coherence_values = []
        model_list = []
        for num_topics in tqdm(range(start, limit, step),desc="LDA-find proper number of topic"):
            model = gensim.models.ldamodel.LdaModel(self.corpus, num_topics=num_topics, id2word=self.dictionary,
                                                    passes=self.passes, random_state=2019)
            model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=self.texts, dictionary=self.dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())

        x = range(start, limit, step)
        # Print the coherence score
        for m, cv in zip(x, coherence_values):
            print("Num Topics =", m, " has Coherence Value of", round(cv, 4))

        self.best_topic_num = x[coherence_values.index(max(coherence_values))]
 
        print("\nbest topic num is {}".format(self.best_topic_num))
</code></pre>

preprocess.py 에서 토큰화된 입력값이 processed_data로 들어오게 되면, init 함수에서 'passes, limit, start, step'의 제한된 파라미터 내에서 최적의 토픽 개수 K를 c_v coherence value값에 따라서 찾아줌. 

Document에 존재하는 단어들이 어떤 topic에 속할 확률이 가장 높은지 계산하여, document 별로 가장 높은 확률의 topic을 찾음
각 토픽별 단어 비중을 확인하여 어떠한 특성을 지닌 주제인지 파악 가능 

<pre><code>
def selected_model(self):
    ...
    ldamodel = gensim.models.ldamodel.LdaModel(self.corpus, num_topics= self.best_topic_num, id2word=self.dictionary,
                                               passes=self.passes, random_state=2019)
    vis = pyLDAvis.gensim.prepare(ldamodel, self.corpus, self.dictionary)
    ...
    return ldamodel, vis

def format_topics_sentences(self, ldamodel,query):
    ...
    sent_topics_df.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    sent_topics_df = sent_topics_df.set_index('Document_No')
    ...
    return sent_topics_df

def extract_index_per_topic(self, ldamodel,query):
    ...
    sent_topics_sorteddf.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text"]
    ...
    return sent_topics_sorteddf
</code></pre>

위의 함수들을 이용해서 LDA 시각화 결과를 html로 만들고, 이슈별 대표 기사 정보를 찾을 수 있음. 자세한 사용법은 main.py에서 


### 0.4 extractive_summarizer.py 
--------------------------
[edubey/text_summarizer](https://github.com/edubey/text-summarizer)의 깃헙을 참고하여 수정하였습니다. 

뉴스 기사 하나의 본문에 대한 내용을 원하는 수의 문장으로 요약

자세한 내용을 알고 싶으신 분들은 [Text_Summarization 관련 repository의 설명글](https://github.com/Hanseok-Oh/Text_Summarization/tree/master/%5B10%5Dcode/edubey_text_summarizer)을 참조해주세요.

