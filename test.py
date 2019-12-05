import pandas as pd
import os
# filename = os.getcwd()+'/data/{}/crawling.xlsx'.format('한화생명')
filename = os.getcwd()+'/data/{}/contents.txt'.format('한화생명')
# df = pd.read_excel(filename,index_col =0)
df = pd.read_csv(filename, sep='\t')

query = '한화생명'
result_path = os.getcwd()+'/data'
def excel_make(query):
    data = pd.read_csv(result_path + '/{}/contents.txt'.format(query), sep='\t', header=None,
                       error_bad_lines=False)
    data.columns = ['years', 'company', 'title', 'contents', 'link']
    out_file = result_path + '/{}/'.format(query) + 'crawling.xlsx'
    data.to_excel(out_file, encoding='utf-8')
    return

excel_make(query)
# for i in range(len(df)):
#     print("{} line:".format(i), len(df.iloc[i,:]))

# print(df.columns)
# print(df.head())
