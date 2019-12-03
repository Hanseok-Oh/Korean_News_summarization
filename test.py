import pandas as pd
import os
# filename = os.getcwd()+'/data/{}/crawling.xlsx'.format('현대중공업')
filename = os.getcwd()+'/data/{}/contents.txt'.format('삼성카드')

# df = pd.read_excel(filename,index_col =0)
df = pd.read_csv(filename, sep='\t')
# print(df.columns)
# print(df.head())

#
# from nltk.cluster.util import cosine_distance
# vector1 =[0,0,1,0,1,1,1]
# vector2 =[0,0,1,0,1,4,0]
# print(round(1 - cosine_distance(vector1, vector2),5))

print(df)