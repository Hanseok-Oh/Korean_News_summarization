'''
기본 코드 구조 참조: https://bumcrush.tistory.com/116
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


class Crawling:
    def __init__(self, max_page, query, s_date, e_date, result_path):
        self.result_path = result_path + '/data'
        self.max_page = max_page
        self.query = query
        self.s_date = s_date
        self.e_date = e_date
        print("crawling: ", self.query)

    def crawler(self):
        s_from = self.s_date.replace(",", "")
        e_to = self.e_date.replace(",", "")
        page = 1
        maxpage_t = (int(self.max_page) - 1) * 10 + 1  # 11= 2페이지 21=3페이지 31=4페이지 ...81=9페이지 , 91=10페이지, 101=11페이지
        f = open(self.result_path + '/{}_contents_text.txt'.format(self.query), 'w',
                 encoding='utf-8')
        while page < maxpage_t:
            print("page:", page)
            # 관련도순 정렬 - query 날짜와 다를 수도 있음 / 수정 필요 부분
            url = "https://search.naver.com/search.naver?where=news&query=" + self.query + "&sort=0&ds=" + self.s_date + "&de=" + self.e_date + "&nso=so%3Adr%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(
                page)
            req = requests.get(url)
            print(url)
            cont = req.content
            soup = BeautifulSoup(cont, 'html.parser')  # print(soup)
            for urls in soup.select("._sp_each_url"):
                try:
                    if urls["href"].startswith("https://news.naver.com"):
                        news_detail = self.get_news(urls["href"])
                        # pdate, pcompany, title, btext
                        f.write(
                            "{}\t{}\t{}\t{}\t{}\n".format(news_detail[1], news_detail[4], news_detail[0],
                                                          news_detail[2],
                                                          news_detail[3]))  # new style
                except Exception as e:
                    print(e)
                    continue
            page += 10
        f.close()
        return

    def get_news(self, n_url):
        news_detail = []
        breq = requests.get(n_url)
        bsoup = BeautifulSoup(breq.content, 'html.parser')
        title = bsoup.select('h3#articleTitle')[0].text  # 대괄호는 h3#articleTitle 인 것중 첫번째 그룹만 가져오겠다.
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

    def excel_make(self, query, date):
        data = pd.read_csv(self.result_path + '/{}_contents_text.txt'.format(query), sep='\t', header=None,
                           error_bad_lines=False)
        data.columns = ['years', 'company', 'title', 'contents', 'link']
        xlsx_outputFileName = '{}.xlsx'.format(query)
        data.to_excel(self.result_path + '/crawling_' + xlsx_outputFileName, encoding='utf-8')
        return

    def main(self):
        self.crawler()  # 검색된 네이버뉴스의 기사내용을 크롤링합니다.
        self.excel_make(self.query, self.s_date + '~' + self.e_date)  # 엑셀로 만들기
        return
