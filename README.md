# Korean_News_summarization
SKKU_TNT 19-2학기 co deeplearning 프로젝트. 


## 1. extractive_summarizer.py
--------------------
뉴스 기사 하나의 본문에 대한 내용을 원하는 수의 문장으로 요약

해당 스크립트 하나만 실행하면 요약 결과 제시

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
