'''
https://data.seoul.go.kr/dataList/OA-15572/S/1/datasetView.do -> 추정매출
https://data.seoul.go.kr/dataList/OA-15560/S/1/datasetView.do -> 영역/상권
'''

import pandas as pd
import os

os.chdir("C:\\Users\\UserK\\Desktop\\Ranee\\SW_CAMP\\태블로를 활용한 시각화\\실습")

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