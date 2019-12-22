import pandas as pd
import os

result_path = os.getcwd().replace("\\",'/')
new_directory = result_path + '/data/{}'.format('카카오')


lda_best = pd.read_excel(new_directory + '/lda_best.xlsx')
target_index=[]
for keys in lda_best['Keywords']:
    target_index.append([keys])
# print("target index:\n", target_index)

summarize_result=[]
f = open(new_directory+'/summary.txt', 'r', encoding='utf-8')
lines = f.readlines()
for line in lines:
    summarize_result.append([line])

f.close()

# print("summarize_result:\n",summarize_result)

temp = [['Summarize Text of topic - 2, index-702: \n'], ['카카오모빌리티는 과학기술정보통신부와 정보통신산업진흥원이 추진하는 인공지능AI 기반 응급의료시스템 개발 사업에 참여 구급차량 전용 내비게이션 및 구급차 출동 안내 서비스를 개발한다고 18일 밝혔다. 119 긴급 출동 알림 서비스를 확대 적용하면 환자 이송 시간을 단축하고 구급 차량과 일반 차량과의 2차 사고 발생 위험을 낮출 수 있을 뿐 아니라 국가 긴급 재해나 재난 발생 시 일반 차량 운전자들의 응급 환자 이송 동참을 유도할 수 있다. 119 긴급 출동 알림 서비스는 카카오내비를 통해 구급 차량 출동 정보와 사고 정보를 일반 차량 운전자들에게 알리는 서비스다\n']]
str = " ".join(temp[0])
print(str)
print("\n ".join(temp[1]).split('.'))

# str = str + " ".join(temp[1]).split('.')

temp=sum(temp,["\n"])
str ="\n".join(temp)

print(str)
