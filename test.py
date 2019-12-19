import re
import pandas as pd
import os
# print(os.getcwd().replace('\\','/'))
df =pd.read_excel(os.getcwd().replace('\\','/')+'/data/카이스트/crawling.xlsx')
for i in range(10):
    temp =df.loc[i,'contents']
    temp2= re.sub('[^\w. ]','',temp)
    print(temp2,"\n")