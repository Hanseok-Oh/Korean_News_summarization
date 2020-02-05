# Korean News Summarization
********************
SKKU_TNT 19-2학기 co deeplearning 및 우수학부연구학점제 주제로 실시한 프로젝트입니다. 

본 프로젝트의 전체적인 프로세스는 
- 1)뉴스기사, 검색어 트랜드 추이, 재무제표 등 데이터 수집 
- 2)LDA 토픽모델링
- 3)문서요약으로 이루어져 있다. 

main.py(version a) 

code flow : dataCrawl -> preprocess -> LDA -> summarization 

최종적으로 특정 기업에 대한 입력이 주어지면 이슈별로 기사분류 및 핵심 내용에 대한 요약 결과 제시를 한다. 이와 더불어서 기업 분석에 도움이 될 검색어 트랜드 추이와 재무제표 데이터를 시각화하여 제시한다. 

본 프로젝트는 실제 주변에 있는 문제 상황을 인식하고 이를 해결하기 위해 기존에 있던 분석 기법들을 활용하여 사회 문제를 해결한다는 의의를 가지며, 실제로 본 모델을 활용한 기업 분석 사례를 제공함으로써 우리 모델이 가지는 완성도와 활용 가능성을 보여준다. 

자세한 설명을 참고하고 싶으면 [공유자료](https://drive.google.com/open?id=17kE1KdiKyJBjpMhrkqV58NT7t7AR3LCX)를 참고하세요. 

![poster](/img/poster.png)

### Web 화면(version b) 예시


- Web 검색 화면 

![Web 검색화면](/img/web1.png)

- Web 기사 이슈별 분류 및 요약 화면
![Web 요약화면](/img/web2.png)

- Web 검색트랜드 제시 화면
![Web 검색트랜드](/img/web3.png)

- Web 재무제표 정보 제시 화면
![Web 재무제표](/img/web4.png)

## Example
------------------
query: 카카오
e_date: 19.06.30

<b>1. issue & keyword</b>
- issue1 : 클레이튼, 블록체인, 서비스, 게임, 플랫폼, 대표, 운영 => 카카오의 블록체인 서비스 운영
- issue2 : 카카오페이, 서비스, 전세금보증, 이용, 가입, 신청, 임대인 => 카카오페이의 전세금보증 서비스
- issue3 : 정보, 서비스, 차량, 마카롱, 자동차, 네비게이션, 사용 => 카카오의 자동차 서비스 관련

LDA 기법을 통한 해당 기간의 뉴스 기사들의 이슈별 분류 및 해당 이슈의 키워드 제시

<b>2. Summarized Text</b>

이슈별 LDA topic contribution이 가장 높은 하나의 대표 문서에 대해서 extractive summarize 제시 

- issue1 : 카카오 모빌리티는 과학기술정보통신부와 정보통신 산업진흥원이 추진하는 인공지능 AI기반 응급 의료 시스템 개발 사업에 참여, 구급차량 전용 내비게이션 및 구급차 출동 안내 서비스를 개발한다고 18일 밝혔다.
- issue2 : 119 긴급 출동 알림 서비스를 확대 적용하면 환자 이송 시간을 단축하고 구급 차량과 일반 차량과의 2차 사고 발생 위험을 낮출 수 있을 뿐 아니라 국가 긴급 재해나 재난 발생 시 일반 차량 운전자들의 응급 환자 이송 동참을 유도할 수 있다.

- issue3 : 119 긴급 출동 알림 서비스는 카카오내비를 통해 구급 차량 출동 정보와 사고 정보를 일반 차량 운전자들에게 알리는 서비스이다.


## Prerequisties
---------------------
- python 3.6
- pip install -r requirements.txt


## How to use
-------------
<pre><code>
  1. git clone https://github.com/Hanseok-Oh/Korean_News_summarization.git
  2. move to directory
  3-a. $python main.py --query <i>검색어</i> 
  3-b. $python Web/pyflask/app.py 
</code></pre>

본 프로젝트의 코드는 두 가지 버젼으로 사용가능합니다. 

a. 웹과 연동하지 않고 디렉토리에 원하는 정보를 담은 파일을 저장. 관심 기업의 뉴스 기사 정보의 이슈분류 및 대표문서에 대한 요약 정보를 제공.

b. Description의 사진 부분과 같이 Web 화면 내에서 프로세스를 진행하여 검색 트랜드, 재무제표 정보를 기업 이슈별 요약 정보와 함께 보는 기능


### main.py의 argparse 부분

<pre><code>
def define_argparser():
    parser = argparse.ArgumentParser(description = 'main argparser')
    parser.add_argument('--query',required=True, help='crawling을 실시할 검색어 명')
    parser.add_argument('--s_date',required=False, default='2019.01.01',help='crawling을 실시할 시작 날짜')
    parser.add_argument('--e_date',required=False, default='2019.03.31',help='crawling을 실시할 끝 날짜')
    parser.add_argument('--result_path',required=False, default=os.getcwd().replace("\\","/"),help='crawling을 완성한 파일을 저장할 위치')
    parser.add_argument('--crawl_only', action='store_true', help='crawling만 실시.')
    parser.add_argument('--page', required=False, default=range(1, 801, 10), type=str, metavar ='range', help='크롤링을 실시할 페이지 수를 입력하세요.')
    parser.add_argument('--LDA_only', action='store_true', help='LDA만 실시.')
    parser.add_argument('--summary_only', action='store_true', help='요약만 진행할 지 여부.')
    parser.add_argument('--index', required=False, default=0, type=int,metavar='N', help='요약을 진행할 txt파일의 index를 입력하시오.')
    parser.add_argument('--number', required=False, default=3, type=int,metavar='N', help='결과로 제시할 문장 수를 입력하시오.')

    args = parser.parse_args()
    return args
</pre></code>


query 정보는 필수로 입력, 나머지 입력값은 help 참고
- 전체 프로세스 진행 모드
<pre><code>
$python main.py --query 카카오 --e_date 2019.06.30
</pre></code>
- 수집된 데이터가 있을 경우 LDA 및 요약 진행 모드
<pre><code>
$python main.py --query 카카오 --LDA_only
</pre></code>
- 요약 결과만 확인 모드
<pre><code>
$python main.py --query 카카오 --summary_only
</pre></code>


## Contact information
---------------------
hanseok.pro@gmail.com

