from elasticsearch import Elasticsearch
import logging
from typing import Any, Dict # 마크표시
import re # 마크를 여러번 표시
import streamlit as st


#인증(아이디, 패스워드)


#elastic server 호출 및 인증




# 데이터 호출 함수
def search_documents_by_keyword(es, index_name, keyword):
    query = {
        "query": {
            "query_string": {
                "query": f"*{keyword}*",
                "default_field": "*"
            }
        }
    }
    try:
        response = es.search(index=index_name, body=query, size=1000)
        return [hit["_source"] for hit in response['hits']['hits']]
    except Exception as e:
        st.error(f"Error occurred in {index_name}: {e}")
        return None

# 키워드 하이라이트 함수
def highlight_keyword(text: str, keyword: str) -> str:
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    highlighted_text = pattern.sub(lambda match: f'<mark style="background-color: yellow;">{match.group(0)}</mark>', text)
    return highlighted_text

def highlight_document(doc: Dict[str, Any], keyword: str) -> Dict[str, Any]:
    highlighted_doc = {}
    for key, value in doc.items():
        if isinstance(value, str):
            highlighted_doc[key] = highlight_keyword(value, keyword)
        elif isinstance(value, list):
            highlighted_doc[key] = [highlight_keyword(item, keyword) if isinstance(item, str) else highlight_document(item, keyword) for item in value]
        elif isinstance(value, dict):
            highlighted_doc[key] = highlight_document(value, keyword)
        else:
            highlighted_doc[key] = value
    return highlighted_doc

# 필드 렌더링 함수
def render_field(key: str, value: Any):
    if isinstance(value, str):
        st.markdown(f"**{key}**: {value}", unsafe_allow_html=True)
    elif isinstance(value, list):
        st.write(f"**{key}**:")
        for item in value:
            if isinstance(item, dict):
                render_field("", item)
            else:
                st.write(item)
    elif isinstance(value, dict):
        st.write(f"**{key}**:")
        for sub_key, sub_value in value.items():
            render_field(sub_key, sub_value)
    else:
        st.write(f"**{key}**: {value}", unsafe_allow_html=True)

# 메인 함수
def main():
    st.title("사업계획서")

    # 사이드바에 검색 부분 배치
    st.sidebar.header("다음을 입력하시오.")
    index_name = st.sidebar.text_input("Name", value="business_plan")
    keyword = st.sidebar.text_input("Keyword")

    if st.sidebar.button("Search"):
        documents = search_documents_by_keyword(es, index_name, keyword)

        if documents:
            st.subheader(f"Documents containing '{keyword}'")
            for doc in documents:
                highlighted_doc = highlight_document(doc, keyword)
                st.markdown("---")
                for key, value in highlighted_doc.items():
                    render_field(key, value)
        else:
            st.error("No documents found containing the keyword")

if __name__ == "__main__":
    main()