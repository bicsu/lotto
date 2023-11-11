import random
from datetime import datetime
from datetime import timedelta
import statistics as stat
import pandas as pd
import requests
import json
from collections import Counter
import pickle
import os

def get_num():
    '''
    1. description :
        get 10 sets of lotto number

    2. parameter
        x
    3. returns
        result_num_list : list, 10 lengths and 2 dimension list array
    '''
    result_num_list = []
    while len(result_num_list) <10 :
        ran_list = random.sample(range(1,46),6)
        if stat.mean(ran_list) >= 20 and stat.mean(ran_list) < 25 :
            ran_list.sort()
            result_num_list.append(ran_list)
        elif stat.stdev(ran_list) >= 12 or stat.stdev(ran_list) < 16 :
            ran_list.sort()
            result_num_list.append(ran_list)
    now_ = datetime.now()
    now_str = f'{now_.year}-{now_.month:02d}-{now_.day:02d}'
    lotto_data = pd.read_csv("./data/lotto_data.csv")
    latest_round = len(lotto_data)
    result_list = [now_str]+result_num_list
    if os.path.isfile(f'./data/nums_thisweek_{latest_round}.pkl') == False:
        with open(f'./data/nums_thisweek_{latest_round}.pkl', 'wb') as f:
            pickle.dump(result_list, f)
    else :
        with open(f'./data/nums_thisweek_{latest_round}.pkl', 'rb') as f:
            result_list = pickle.load(f)
    return result_list[1:]


from datetime import datetime, timedelta

def get_date():
    '''
    1. description:
        Get today and the upcoming Saturday (lotto day).
    2. parameters:
        None
    3. returns:
        today_str : str, yyyy-mm-dd
        saturday : str, yyyy-mm-dd
    '''

    now_ = datetime.now()
    today_str = now_.strftime('%Y-%m-%d')

    d = datetime.today()
    sat_offset = 5 - d.weekday()

    if sat_offset <= 0:
        sat_offset += 7

    saturday = d + timedelta(days=sat_offset)
    saturday_str = saturday.strftime('%Y-%m-%d')

    print("Today:", today_str)
    print("Next Saturday:", saturday_str)

    return today_str, saturday_str

today, next_saturday = get_date()





def lottodataUpdate():
    lotto_data = pd.read_csv("./data/lotto_data.csv")
    minDrwNo = len(lotto_data)       #취득하고 싶은 회차 시작
    maxDrwNo = len(lotto_data)+1        #취득하고 싶은 회차 종료
    drwtNo1 = []        #1등 첫번째 번호
    drwtNo2 = []        #1등 두번째 번호
    drwtNo3 = []        #1등 세번째 번호
    drwtNo4 = []        #1등 네번째 번호
    drwtNo5 = []        #1등 다섯번째 번호
    drwtNo6 = []        #1등 여섯번째 번호
    bnusNo = []         #1등 보너스 번호
    drwNoDate = []      #로또 추첨일

    # 지정한 시작 회차 부터 종료 회차 까지 취득
    try :
        for i in range(minDrwNo, maxDrwNo + 1, 1):
            # 1등 번호를 취득
            req_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i)

            req_lotto = requests.get(req_url)

            lottoNo = req_lotto.json()

            drwNoDate.append(lottoNo['drwNoDate'])  # 로또 추첨일
            drwtNo1.append(lottoNo['drwtNo1'])      #1등 첫번째 번호 저장
            drwtNo2.append(lottoNo['drwtNo2'])      #1등 두번째 번호 저장
            drwtNo3.append(lottoNo['drwtNo3'])      #1등 세번째 번호 저장
            drwtNo4.append(lottoNo['drwtNo4'])      #1등 네번째 번호 저장
            drwtNo5.append(lottoNo['drwtNo5'])      #1등 다섯번째 번호 저장
            drwtNo6.append(lottoNo['drwtNo6'])      #1등 여섯번째 번호 저장
            bnusNo.append(lottoNo['bnusNo'])   #1등 보너스 번호 저장
    except :
        print("Round counting error please check data and check the current lotto round")

    lotto_dict = {"추첨일":drwNoDate, "Num1":drwtNo1, "Num2":drwtNo2, "Num3":drwtNo3, "Num4":drwtNo4, "Num5":drwtNo5, "Num6":drwtNo6, "bnsNum":bnusNo,}
    df_lotto_toadd = pd.DataFrame(lotto_dict)

    if len(df_lotto_toadd) != 0 :
        lotto_data = pd.concat([lotto_data, df_lotto_toadd]).drop_duplicates()
        lotto_data.to_csv(f"./data/lotto_data.csv", index=False)


    print('New data updated Done')