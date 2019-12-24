'''
기본 코드 구조 참조: https://bumcrush.tistory.com/116
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd

class Crawling:
    def __init__(self, query, s_date, e_date, result_path):
        self.result_path = result_path + '/data'
        self.query = query
        self.s_date = s_date
        self.e_date = e_date
        self.article_links=[]
        print("crawling: ", self.query)

    def crawler(self, page):
        s_from = self.s_date.replace(".", "")
        e_to = self.e_date.replace(".", "")
        query = self.query
        f = open(self.result_path + '/{}/contents.txt'.format(self.query), 'a',
                 encoding='utf-8')

        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=" + self.s_date + "&de=" + self.e_date + "&docid=&nso=so:r,p:from" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)

        req = requests.get(url)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')

        for urls in soup.select("._sp_each_url"):
            try:
                if urls["href"].startswith("https://news.naver.com"):
                    news_detail = self.get_news(urls["href"])
                    # 중복 기사 링크 제거
                    if news_detail[3] in self.article_links:
                        continue
                    else:
                        self.article_links.append(news_detail[3])

                    reversed_content_2 = ''.join(reversed(news_detail[2]))
                    for i in range(0, len(reversed_content_2)):
                        if reversed_content_2[i:i + 2] == '.다':
                            news_detail[2] = ''.join(reversed(reversed_content_2[i:]))
                            break
                    for i in range(0, int(len(news_detail[2]) / 3)):
                        if news_detail[2][i:i+3] == '기자]' or news_detail[2][i:i+3] == '자 =':
                            news_detail[2] = news_detail[2][i+3:]
                            break
                        if news_detail[2][i:i+4] == ' 기자 ':
                            news_detail[2]=news_detail[2][i+4:]
                            break


                    if 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=024&aid=0000061805' in news_detail:
                        news_detail[2] = news_detail[2].replace('\r', '')
                        # pass
                    if len(news_detail[2].split('.'))<5:
                        continue

                    if ']' in news_detail[2][:len(news_detail[2]) // 4]:
                        temp = news_detail[2].split(']')[1:]  # 기사 앞 [기자이름] 부분 제거
                        news_detail[2] = ' '.join(temp)

                    if type(news_detail[2])!=str or len(news_detail[2])<2: # contents가 비어있을 경우 float type :nan
                        continue

                    f.write(
                        "{}\t{}\t{}\t{}\t{}\n".format(news_detail[1], news_detail[4], news_detail[0],
                                                      news_detail[2],
                                                      news_detail[3]))  # years, company, title, contents, link
            except Exception as e:
                # print(e)
                continue
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

    def excel_make(self, query):
        data = pd.read_csv(self.result_path + '/{}/contents.txt'.format(query), sep='\t', header=None,
                           error_bad_lines=False)
        data.columns = ['years', 'company', 'title', 'contents', 'link']
        out_file = self.result_path + '/{}/'.format(query) + 'crawling.xlsx'
        data.to_excel(out_file, encoding='utf-8')
        return

    def main(self, page):
        self.crawler(page)
        self.excel_make(self.query)
        return
