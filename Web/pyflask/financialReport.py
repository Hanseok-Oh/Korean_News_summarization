import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as fm
import os

#사용자 설정에서 폰트 배포 필요
font_location = "C:/Users/rnfek/miniconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/NanumSquareR.ttf"
font_name = fm.FontProperties(fname=font_location).get_name()
mpl.rc('font',family=font_name)

result_path = os.getcwd().replace("\\", '/')
new_directory = result_path + '/Web/pyflask/static/images/Report/'



class MakeReport:
    '''
    find_code -> make_data -> remake_df
    '''
    def __init__(self,args):
        self.query = args.query
        self.base_URL = "https://finance.naver.com/item/main.nhn?code="


    def find_code(self,query):
        df = pd.read_excel('sub_data/company_code.xlsx',skiprows=3)
        df = df.loc[(df['업종명'] == 'KOSPI') | (df['업종명'] == 'KOSDAQ'), :]
        try:
            temp_code = df.loc[df['종목명'] == query, '종목코드'].values[0] # series 데이터는 idex, value의 값을 지닌다.
            code = temp_code.replace("'", "")

        except:
            code =None
            print("There is no code for requested query.")

        return code

    def remake_df(self, df):
        #dataframe 형태 변형
        index = []
        for j in df.index:
            for i in range(len(df.columns)):
                index.append(j)

        name = []
        for i in range(len(df.index)):
            for j in df.columns:
                name.append(j)

        value = []
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                value.append(df.iloc[i, j])

        return index,name,value

    def make_data(self):
        code = self.find_code(self.query)
        if code== None:
            return -1

        URL = self.base_URL + code
        target_company = requests.get(URL)
        html = target_company.text
        soup = BeautifulSoup(html, 'html.parser')
        finance_html = soup.select('div.section.cop_analysis div.sub_section')[0]
        th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
        annual_date = th_data[3:7]
        quarter_date = th_data[7:13]

        finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:]
        finance_data = [item.get_text().strip() for item in finance_html.select('td')]
        finance_data = np.array(finance_data)
        finance_data.resize(len(finance_index), 10)

        finance_date = annual_date + quarter_date
        finance = pd.DataFrame(data=finance_data[0:,0:], index=finance_index, columns=finance_date)

        annual_finance = finance.iloc[:, :4]
        quarter_finance = finance.iloc[:, 4:]

        df = np.transpose(quarter_finance.iloc[0:5, :])
        df = np.transpose(quarter_finance.iloc[0:5, :])
        df[['영업이익률', '순이익률']] = df[['영업이익률', '순이익률']].apply(pd.to_numeric)
        df['영업이익'] = df.영업이익.str.replace(',', '').astype('int64')
        df['매출액'] = df.매출액.str.replace(',', '').astype('int64')
        df['당기순이익'] = df.당기순이익.str.replace(',', '').astype('int64')

        # 당기순이익 너무 값이 커서 10으로 나눔
        df.iloc[:,0] = df.iloc[:,0]/10

        # df2 매출액 영업이익 당기순이익
        df2 = df.iloc[:,0:3]

        index,name,value = self.remake_df(df2)
        new_df = pd.DataFrame({'Date': index, 'FinancialStatements': name, 'Value': value})

        # df3 영업이익률 당기순익률
        df3 = df.iloc[:,3:5]

        index,name,value = self.remake_df(df3)
        new_df2 = pd.DataFrame({'Date':index,'Profit':name,'Value':value})

        return new_df,new_df2


    def plot_report(self,new_df,new_df2):
        sns.barplot(x='Date', y='Value', hue='FinancialStatements', data=new_df) # default : dodge=True
        plt.title('FinancialStatements', fontsize=20)
        plt.ylabel('one hundred million', fontsize = 10)
        plt.legend(fontsize=5,loc=1)

        plt.twinx()
        sns.lineplot(x='Date',  y='Value', hue='Profit',data=new_df2)
        plt.ylabel('Percent', fontsize=10)
        plt.legend(fontsize=7,loc=7)
        plt.savefig(new_directory + "{}_report.png".format(self.query))
        print("financial report is saved in the directory\n")


    def make_plot(self):
        if self.make_data() == -1:
            return -1
        else:
            new_df,new_df2 = self.make_data()
            if os.path.exists(new_directory+"{}_report.png".format(self.query)):
                print("already exists")
                return 0
            else:
                self.plot_report(new_df,new_df2)
                return 0
