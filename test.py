# coding=utf-8
# {}_요약.txt 파일에서 문서별로 배정된 key& 인덱스 정보를 파악

# f = open('data/삼성생명_요약.txt','r',encoding='utf-8')
# lines = f.readlines()
# temp = []
# for line in lines:
#     if 'key' in line:
#         print(line)
#         temp.append((line[0],line[-2]))
#
# print("temp: ",temp)
#
from collections import Counter

cnt = Counter()
for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
    cnt[word] += 1

print(cnt)
print(cnt.most_common(1))
print(cnt.most_common(1)[0][0])