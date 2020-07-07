# https://financedata.github.io/posts/finance-data-reader-users-guide.html

# 설명 https://blog.naver.com/boot/221973650672
import FinanceDataReader as fdr
import datetime
from time import time, sleep
from notifier import *

max_diff = 0
loop_count = 0
while True:
    # 시작 시간
    start_time = time()

    today = datetime.datetime.now()
    year = datetime.timedelta(days=365)
    year_ago = today - year

    # 1년 전
    year_ago = year_ago.strftime('%Y-%m-%d')
    today = today.strftime('%Y-%m-%d')

    '''
    1. 원달러환율 계산 
    '''
    # 원달러환율 정보 (1년전 ~ 오늘)
    df_exchange_rate = fdr.DataReader('USD/KRW', year_ago, today)

    # 원달러환율 현재
    current_exchange_rate = df_exchange_rate[-1:]['Close'][0]

    # 원달러환율 (1년전 ~ 오늘) 최대, 최소
    highest_exchange_rate_idx = df_exchange_rate.High.idxmax()
    lowest_exchange_rate_idx = df_exchange_rate.Low.idxmin()

    # 원달러환율 1년 사이 최대 + 최소 / 2 = 평균값 계산
    exchange_rate_avg = (df_exchange_rate.loc[highest_exchange_rate_idx, 'High'] + df_exchange_rate.loc[
        lowest_exchange_rate_idx, 'Low']) / 2

    '''
    2. 달러지수 계산 
    '''
    # 달러지수 정보 (1년전 ~ 오늘)
    df_DXY = fdr.DataReader('DXY', year_ago, today)

    # 달러지수 현재
    current_dollar_idx = df_DXY[-1:]['Close'][0]

    # 달러지수 (1년전 ~ 오늘) 최대, 최소
    highest_dollar_idx = df_DXY.High.idxmax()
    lowest_dollar_idx = df_DXY.Low.idxmin()

    # 달러지수 1년 사이 최대 + 최소 / 2 = 평균값 계산
    dollar_idx_avg = (df_DXY.loc[highest_dollar_idx, 'High'] + df_DXY.loc[lowest_dollar_idx, 'Low']) / 2

    # 평균 달러지수/환율
    avg_ratio = dollar_idx_avg / exchange_rate_avg * 100

    # 현재 달러지수/환율
    current_ratio = current_dollar_idx / current_exchange_rate * 100

    # 적정환율
    proper_exchange_rate = current_dollar_idx / avg_ratio * 100

    # 적정환율 - 현재환율 갭
    diff_exchange_rate = (proper_exchange_rate - current_exchange_rate) / current_exchange_rate * 100

    print('???')
    # 현재 환율이 적정환율보다 적고 현재 환율과 적정환율 사이 차이가 제일 클 때 알림 전송
    if current_exchange_rate < proper_exchange_rate and diff_exchange_rate > max_diff:
        max_diff = diff_exchange_rate
        message = '\n  0. 현재환율: ' + str(current_exchange_rate)
        message += '\n 1. 평균환율: ' + str(exchange_rate_avg)
        message += '\n 2. 현재 달러지수: ' + str(current_dollar_idx)
        message += '\n 3. 평균 달러지수: ' + str(dollar_idx_avg)
        message += '\n 4. 현재 달러지수/환율: ' + str(current_ratio)
        message += '\n 5. 평균 달러지수/환율: ' + str(avg_ratio)
        message += '\n 6. 적정환율: ' + str(proper_exchange_rate)
        message += '\n 7. 적정환율 - 현재환율 갭: ' + str(diff_exchange_rate)

        # 알림 메세지 전송
        send_message_by_line(message)

        # print summary
        print('0. 현재환율', current_exchange_rate)
        print('1. 평균환율', exchange_rate_avg)
        print('2. 현재 달러지수', current_dollar_idx)
        print('3. 평균 달러지수', dollar_idx_avg)
        print('4. 현재 달러지수/환율', current_ratio)
        print('5. 평균 달러지수/환율', avg_ratio)
        print('6. 적정환율', proper_exchange_rate)
        print('7. 적정환율 - 현재환율 갭', (proper_exchange_rate - current_exchange_rate) / current_exchange_rate * 100)
        sleep(120)
    else:
        sleep(300)  # 5분마다 한번씩 알림

    loop_count += 1
    if loop_count % 50 == 0:
        # 초기화
        max_diff = 0

    # 종료시간
    end_time = time() - start_time
    print(end_time)


