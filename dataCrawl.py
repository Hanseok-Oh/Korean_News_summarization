'''
기본 코드 구조 참조: https://bumcrush.tistory.com/116
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# crawling된 파일을 저장할 경로를 입력
RESULT_PATH = 'C:/Users/rnfek/hanseok/Text_Summarization/[10]code/data'
now = datetime.now()

def crawler(maxpage, query, s_date, e_date):
    '''
    :param maxpage: 보고 싶은 페이지묶음 + 1
    :param query: 검색할 문자를 입력
    :param s_date: 뉴스를 긁어모으기 시작할 날짜
    :param e_date: 뉴스를 긁어모을 마지막 날짜
    :return: None
    '''
    s_from = s_date.replace(",","")
    e_to = e_date.replace(",","")
    page = 1
    maxpage_t = (int(maxpage)-1)*10+1 # 11= 2페이지 21=3페이지 31=4페이지 ...81=9페이지 , 91=10페이지, 101=11페이지
    f = open( 'C:/Users/rnfek/hanseok/Text_Summarization/[10]code/data/{}_contents_text.txt'.format(query), 'w', encoding='utf-8')
    while page < maxpage_t:
        print("page:",page)
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=0&ds=" + s_date + "&de=" + e_date + "&nso=so%3Add%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(
            page)
        req = requests.get(url)
        print(url)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')  # print(soup)
        for urls in soup.select("._sp_each_url"):
            try:
                # print(urls["href"])
                if urls["href"].startswith("https://news.naver.com"):
                    # print(urls["href"])
                    news_detail = get_news(urls["href"])
                    # pdate, pcompany, title, btext
                    f.write(
                        "{}\t{}\t{}\t{}\t{}\n".format(news_detail[1], news_detail[4], news_detail[0], news_detail[2],
                                                      news_detail[3]))  # new style
            except Exception as e:
                print(e)
                continue
        page += 10
    f.close()

def get_news(n_url):
    news_detail = []
    breq = requests.get(n_url)
    bsoup = BeautifulSoup(breq.content, 'html.parser')
    title = bsoup.select('h3#articleTitle')[0].text #대괄호는 h3#articleTitle 인 것중 첫번째 그룹만 가져오겠다.
    news_detail.append(title)
    pdate = bsoup.select('.t11')[0].get_text()[:11]
    news_detail.append(pdate)
    _text = bsoup.select('#articleBodyContents')[0].get_text().replace('\n', " ")
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")
    news_detail.append(btext.strip())
    news_detail.append(n_url)
    pcompany = bsoup.select('#footer address')[0].a.get_text()
    news_detail.append(pcompany)
    return news_detail

def excel_make(query,date):
    data = pd.read_csv(RESULT_PATH+'/{}_contents_text.txt'.format(query), sep='\t',header=None, error_bad_lines=False)
    data.columns = ['years','company','title','contents','link']
    print(data)
    # xlsx_outputFileName = '%s-%s-%s %s시 %s분 %s초 result.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    xlsx_outputFileName = '{}_{}.xlsx'.format(query,date)

    #xlsx_name = 'result' + '.xlsx'
    data.to_excel(RESULT_PATH+'/crawling_'+xlsx_outputFileName, encoding='utf-8')


def main():
    maxpage = input("최대 출력할 페이지수 입력하시오: ")
    query = input("검색어 입력: ")
    s_date = input("시작날짜 입력(ex.2019.01.01):")  # 2019.01.01
    e_date = input("끝날짜 입력(ex.2019.04.28):")  # 2019.04.28
    crawler(maxpage, query, s_date, e_date)  # 검색된 네이버뉴스의 기사내용을 크롤링합니다.
    excel_make(query,s_date +'~'+ e_date)  # 엑셀로 만들기


main()

