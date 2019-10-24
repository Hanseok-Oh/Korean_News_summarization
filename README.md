# Korean_News_summarization
SKKU_TNT 19-2학기 co deeplearning 프로젝트. 


## 0. models
code flow : dataCrawl -> preprocess -> LDA -> summarization

### 0.1 dataCrawl.py
------------------
[bumcrush 님의 기본 코드 구조](https://bumcrush.tistory.com/116)를 참조하여 적용했습니다. 


<pre><code> 
  def main():
      maxpage = input("최대 출력할 페이지수 입력하시오: ")
      query = input("검색어 입력: ")
      s_date = input("시작날짜 입력(ex.2019.01.01):")  # 2019.01.01
      e_date = input("끝날짜 입력(ex.2019.04.28):")  # 2019.04.28
      crawler(maxpage, query, s_date, e_date)  # 검색된 네이버뉴스의 기사내용을 크롤링합니다.
      excel_make(query,s_date +'~'+ e_date)  # 엑셀로 만들기
</code></pre>
    
    
main 함수는 다음과 같이 작동합니다.
 
- maxpage:  10개 단위로 출력할 페이지 묶음 수
- query : 네이버 뉴스에서 긁어모을 기사의 키워드
- s_date / e_date : 기사를 긁어모으길 시작할 날짜와 중단할 날짜

=> years, company(언론사), title, contents, link 의 column에 맞춰서 

RESULT_PATH+'/{}_contents_text.txt'.format(query) 형태로 파일이 저장됨 

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

## 1. extractive_summarizer.py ( in progress)
--------------------
뉴스 기사 하나의 본문에 대한 내용을 원하는 수의 문장으로 요약

해당 스크립트 하나만 실행하면 요약 결과 제시

[edubey/text_summarizer](https://github.com/edubey/text-summarizer)의 깃헙을 참고하여 수정하였습니다. 

자세한 내용을 알고 싶으신 분들은 [본 깃헙내 설명글](https://github.com/Hanseok-Oh/Text_Summarization/tree/master/%5B10%5Dcode/edubey_text_summarizer)을 참조해주세요.

### 1.1 How to use
-------------

  1. git clone https://github.com/Hanseok-Oh/Korean_News_summarization.git
  2. move to directory
  3. put the target file into the 'data/articles_content/' directory.
  4. <b> python extractive_summarizer.py --file_name = FILE_NAME --number = NUMBER </b>

  - 요약을 실시하고자 하는 파일을 'data/articles_content/FILE_NAME' 형태로 넣어둔다. 형식은 txt 파일
  - 결과로 요약하고자 하는 문장 수를 입력 : NUMBER (default 2)


-----------------------
파일명 & 요약할 문장 수

  optional arguments:
  
  -h, --help            show this help message and exit
  
  --file_name FILE_NAME  요약을 진행할 txt파일명을 입력하시오.                       
                        
  --number NUMBER       결과로 제시할 문장 수를 입력하시오.

