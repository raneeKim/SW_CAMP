
import json
import streamlit as st
from elasticsearch import Elasticsearch, NotFoundError, ConnectionError
from PIL import Image, ImageDraw, ImageFont
import logging
import matplotlib.pyplot as plt

# 인증(아이디, 패스워드)
def login():
    username = 'elastic'
    password = 'GQyuqSbBJEzbk6vAKT53'
    return (username, password)

# elastic server 호출 및 인증
es = Elasticsearch(
    ['http://1.213.180.227:9200/'],
    basic_auth=login())


## Elasticsearch에서 데이터 가져오기
def fetch_data(es, index_name, doc_id):
    try:
        response = es.get(index=index_name, id=doc_id)
        return response['_source']
    except NotFoundError:
        st.error(f"Document ID '{doc_id}'를 찾을 수 없습니다.")
    except ConnectionError:
        st.error("Elasticsearch에 연결할 수 없습니다.")
    return None

# 중첩된 데이터를 키를 통해 추출하는 함수
def get_nested_value(data, keys):
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        else:
            return None
    return data

# 데이터를 시각화하는 함수
def render_graph(market_con_data):
    if not market_con_data:
        st.error("Market condition data is not available.")
        return

    years = list(market_con_data.keys())
    values = list(market_con_data.values())

    fig, ax = plt.subplots()
    ax.plot(years, values, marker='o')

    ax.set_xlabel('Year')
    ax.set_ylabel('Value')
    ax.set_title('Market Condition Over Years')

    st.pyplot(fig)

# 메인 함수
def main():
    st.title("Market Condition Graph")

    # 사용자 입력
    index_name = st.text_input("Enter index name:", value="your_index_name")
    doc_id = st.text_input("Enter document ID:", value="your_document_id")

    if st.button("Fetch and Plot Data"):
        data = fetch_data(es, index_name, doc_id)
        
        if not data:
            st.error("No data found.")
            return
        
        market_con_data = get_nested_value(data, ["market_con", 0])  # market_con 리스트의 첫 번째 항목
        if market_con_data:
            render_graph(market_con_data)
        else:
            st.error("No market condition data found.")

if __name__ == "__main__":
    main()