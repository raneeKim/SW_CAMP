'''
https://data.seoul.go.kr/dataList/OA-15572/S/1/datasetView.do -> 추정매출
https://data.seoul.go.kr/dataList/OA-15560/S/1/datasetView.do -> 영역/상권
'''

import pandas as pd
import os
import numpy as np
os.getcwd()

os.chdir(r"C:\Users\UserK\Desktop\Ranee\SW_CAMP\태블로를 활용한 시각화\실습")
os.chdir("C:\\Users\\MSI\\Desktop\\study\\SW_CAMP\\태블로를 활용한 시각화\\실습")

mainn = pd.read_csv("서울시 상권분석서비스(추정매출-상권).csv", encoding='cp949')
namee = pd.read_csv("서울시 상권분석서비스(영역-상권).csv", encoding='cp949')
namee.info()
mainn.head()
mainn.info()
namee = namee[['상권_코드','자치구_코드_명']]
namee

result = pd.merge(mainn,namee,on='상권_코드',how='left')
result.isna().sum() # 널값확인

result.to_csv('최종파일.csv',encoding='cp949')




result = pd.read_csv("서울시 상권분석서비스(추정매출-자치구).csv", encoding='cp949')
result.info()
result.loc[result['기준_년분기_코드'] == 20191 , '기준_년분기_코드'] = '2019-02-01'
result.loc[result['기준_년분기_코드'] == 20192 , '기준_년분기_코드'] = '2019-05-01'
result.loc[result['기준_년분기_코드'] == 20193 , '기준_년분기_코드'] = '2019-08-01'
result.loc[result['기준_년분기_코드'] == 20194 , '기준_년분기_코드'] = '2019-11-01'

result.loc[result['기준_년분기_코드'] == 20201 , '기준_년분기_코드'] = '2020-02-01'
result.loc[result['기준_년분기_코드'] == 20202 , '기준_년분기_코드'] = '2020-05-01'
result.loc[result['기준_년분기_코드'] == 20203 , '기준_년분기_코드'] = '2020-08-01'
result.loc[result['기준_년분기_코드'] == 20204 , '기준_년분기_코드'] = '2020-11-01'

result.loc[result['기준_년분기_코드'] == 20211 , '기준_년분기_코드'] = '2021-02-01'
result.loc[result['기준_년분기_코드'] == 20212 , '기준_년분기_코드'] = '2021-05-01'
result.loc[result['기준_년분기_코드'] == 20213 , '기준_년분기_코드'] = '2021-08-01'
result.loc[result['기준_년분기_코드'] == 20214 , '기준_년분기_코드'] = '2021-11-01'

result.loc[result['기준_년분기_코드'] == 20221 , '기준_년분기_코드'] = '2022-02-01'
result.loc[result['기준_년분기_코드'] == 20222 , '기준_년분기_코드'] = '2022-05-01'
result.loc[result['기준_년분기_코드'] == 20223 , '기준_년분기_코드'] = '2022-08-01'
result.loc[result['기준_년분기_코드'] == 20224 , '기준_년분기_코드'] = '2022-11-01'

result.loc[result['기준_년분기_코드'] == 20231 , '기준_년분기_코드'] = '2023-02-01'
result.loc[result['기준_년분기_코드'] == 20232 , '기준_년분기_코드'] = '2023-05-01'
result.loc[result['기준_년분기_코드'] == 20233 , '기준_년분기_코드'] = '2023-08-01'

result.head()
result.tail()

result.to_csv('최종파일.csv',encoding='cp949')


result = pd.read_csv("최종파일.csv", encoding='cp949')
result.columns.to_list()


df1 = result.melt(id_vars = ['기준_년분기_코드', '자치구_코드_명', '서비스_업종_코드_명', '당월_매출_금액', '당월_매출_건수', '주중_매출_금액', '주말_매출_금액',
                             '00시~06시', '06시~11시', '11시~14시', '14시~17시', '17시~21시', '21시~24시', 
                             '남성_매출_금액', '여성_매출_금액', '10대', '20대', '30대', '40대', '50대', '60대 이상'] ,
                        value_vars=['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'],
                        var_name='요일',
                        value_name='요일별_매출_금액')

df1.info()
df1.columns.to_list()


df2 = df1.melt(id_vars = ['기준_년분기_코드', '자치구_코드_명', '서비스_업종_코드_명', '당월_매출_금액', '당월_매출_건수', '주중_매출_금액', '주말_매출_금액', 
                          '00시~06시', '06시~11시', '11시~14시', '14시~17시', '17시~21시', '21시~24시', '남성_매출_금액', '여성_매출_금액', '요일', '요일별_매출_금액'] ,
                        value_vars=['10대', '20대', '30대', '40대', '50대', '60대 이상'],
                        var_name='나이',
                        value_name='나이별_매출_금액')

df2.info()
df2.columns.to_list()

df3 = df2.melt(id_vars = ['기준_년분기_코드', '자치구_코드_명', '서비스_업종_코드_명', '당월_매출_금액', '당월_매출_건수', '주중_매출_금액', '주말_매출_금액', 
                          '남성_매출_금액', '여성_매출_금액', '요일', '요일별_매출_금액'] ,
                        value_vars=['00시~06시', '06시~11시', '11시~14시', '14시~17시', '17시~21시', '21시~24시'],
                        var_name='시간대',
                        value_name='시간대별_매출_금액')

df3.to_csv('최종파일2.csv', encoding='cp949')
