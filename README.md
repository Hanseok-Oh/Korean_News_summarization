# Korean_News_summarization
SKKU_TNT 19-2학기 co deeplearning 프로젝트. 


## 0. models (in progress)
code flow : dataCrawl -> preprocess -> LDA -> summarization 

## 1. main.py 
------------------

전체 프로세스를 진행하는 script

query 정보는 필수로 입력 

(ex. 현대자동차, 11번가 등의 검색할 키워드 / 원하는 결과 조합 가능 : 현대자동차+취업)

<pre><code>
def define_argparser():
    parser = argparse.ArgumentParser(description = 'main argparser')
    parser.add_argument('--max_page',required=False,default=50,help= 'crawling을 실시할 페이지 수')
    parser.add_argument('--query',required=True, help='crawling을 실시할 검색어 명')
    parser.add_argument('--s_date',required=False, default='2019.01.01',help='crawling을 실시할 시작 날짜')
    parser.add_argument('--e_date',required=False, default='2019.03.31',help='crawling을 실시할 끝 날짜')
    parser.add_argument('--result_path',required=False,     default='C:/Users/rnfek/hanseok/Korean_News_summarization/',help='crawling을 완성한 파일을 저장할 위치')
    # parser.add_argument('--file_name', required=True, help='요약을 진행할 txt파일명을 입력하시오.')
    parser.add_argument('--index', required=False, default=0, type=int, help='요약을 진행할 txt파일의 index를 입력하시오.')
    parser.add_argument('--number', required=False, default=2, type=int, help='결과로 제시할 문장 수를 입력하시오.')
    args = parser.parse_args()
    return args

</pre></code>


### 1.1 How to use
-------------

  1. git clone https://github.com/Hanseok-Oh/Korean_News_summarization.git
  2. move to directory
  3. <b> python main.py --query 현대자동차 </b>

