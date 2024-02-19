import pandas as pd
from gemini_handler import GeminiAPI
import time

# 자소서 데이터 불러오기
self_introduction = pd.read_csv('./self_introductions/self_introduction_worknet_2016.csv')

# 평가지표 데이터 불러오기
guide = pd.read_json('./guides/grading_2016.json')

# gemini api 객체 생성
api = GeminiAPI()

# 자소서 데이터를 문항 단위로 분리하는 함수
def parsing(self_introduction) -> list:
    ex = self_introduction.split('\n')
    first = ''
    second = ''
    third = ''
    i = 0
    while True:
        if '삼성취업을 선택한 이유와 입사' in ex[i]:
            while True:
                first += ex[i+1]
                i += 1
                if '본인의 성장과정을 간략히 기술' in ex[i+1]:
                    break
        elif '본인의 성장과정을 간략히 기술' in ex[i]:
            while True:
                second += ex[i+1]
                i += 1
                if '최근 사회이슈 중 중요하다고 생각되는 한가지' in ex[i+1]:
                    break
        elif '최근 사회이슈 중 중요하다고 생각되는 한가지' in ex[i]:
            while True:
                third += ex[i+1]
                i += 1
                if i+1 == len(ex):
                    break   
        else:
            i += 1
        if i+1 == len(ex):
            break
    return [first , second , third]

# 문항별 응답 분리
self_introduction = self_introduction['self_intro'].apply(lambda x: parsing(x))


# 두 자소서 평가에 대해 기록하는 dataframe 생성
recodings = pd.DataFrame(columns=['A 자소서', 'B 자소서','문항','평가지표','승자','패자'])

# 매 문항마다 두 자소서를 비교
num = 0
for i in range(len(self_introduction)):
    for j in range(len(self_introduction)):
        if i < j:
            # 두 자소서를 불러오기
            a = self_introduction.iloc[i]
            b = self_introduction.iloc[j]
            
            for k in range(len(guide)):
                q = guide.iloc[k]
                question = q['question']
                metrics= q['grading']
                # 두 자소서의 문항에 대해 평가지표를 비교
                for l in range(len(metrics)):
                    metric = metrics[l]
                    try:
                        result = api.gradings(metric, a[k], b[k])
                    except:
                        print('list index (0) out of range')
                        time.sleep(3)
                        print('error')
                        result = 'None'
                        recodings.loc[num] = [a[k], b[k], question, metric, 'error', 'error']
                        continue
                    
                    # result를 /data8/auto-prompt/gemini_handler/results에 result_num.txt저장
                    with open('./result/result_'+str(num)+'.txt', 'w') as f:
                        f.write(result)
                    # result를 recodings에 기록
                    # result의 첫줄이 1이면 A자소서가 더 좋은 것, 2이면 B자소서가 더 좋은
                    if result.split('\n')[0] == '1':
                        recodings.loc[num] = [a[k], b[k], question, metric, i, j]
                    elif result.split('\n')[0] == '2':
                        recodings.loc[num] = [a[k], b[k], question, metric, j, i]
                    else:
                        recodings.loc[num] = [a[k], b[k], question, metric, '보류', '보류']
                    print(num)
                    print(metric, a[k], b[k])
                    num += 1
                    recodings.to_csv('./result/recodings_samsung_2016.csv', index=False)