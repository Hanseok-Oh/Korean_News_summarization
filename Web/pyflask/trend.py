import urllib.request
import simplejson as json
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
font_location = "C:/Users/rnfek/miniconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/NanumSquareR.ttf"
font_name = fm.FontProperties(fname=font_location).get_name()
mpl.rc('font',family=font_name)



client_id = "GFvC5k1JjrORTMcWco2s"
client_secret = "D3NVvgLDl1"
result_path = os.getcwd().replace("\\", '/')
new_directory = result_path + '/Web/pyflask/static/images/Trends/'


class SearchTrend:
    def __init__(self,args):
        self.query = args.query
        self.body_dict = {
                    "startDate":args.s_date.replace('.','-'),
                    "endDate":args.e_date.replace('.','-'),
                    "timeUnit":"date",
                    "keywordGroups":[
                        {"groupName":args.query,"keywords":[args.query]}, #keywords에 여러 기업 입력 가능
                                    ]}
        self.body =json.dumps(self.body_dict, indent=4, ensure_ascii=False)


    def get_trend(self):
        url = "https://openapi.naver.com/v1/datalab/search"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        request.add_header("Content-Type", "application/json")
        response = urllib.request.urlopen(request, data=self.body.encode("utf-8"))
        return json.loads(response.read().decode('utf-8'))


    def plotTrend(self):

        raw_data = self.get_trend()
        ratio = [each['ratio'] for each in raw_data['results'][0]['data']]
        date = [each['period'] for each in raw_data['results'][0]['data']]

        date = pd.to_datetime(date)
        plt.figure(figsize=(20, 10))
        plt.plot(date, ratio, linestyle='-', color='r')

        plt.title("{} Search Trend".format(self.query),fontsize=20)
        plt.xlabel('Date', fontsize=15)
        plt.ylabel('Frequency ratio', fontsize=15)
        plt.savefig(new_directory + "{}_trend.png".format(self.query))
