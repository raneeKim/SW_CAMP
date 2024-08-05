import json
import streamlit as st
from elasticsearch import Elasticsearch, NotFoundError, ConnectionError
from PIL import Image, ImageDraw, ImageFont
import logging
import pandas as pd
import plotly.express as px

# 인증(아이디, 패스워드)
def login():
    username = 'elastic'
    password = '*****'
    return (username, password)

# elastic server 호출 및 인증
es = Elasticsearch(
    ['*******'],
    basic_auth=login())

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# JSON 파일을 로드하는 함수
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("JSON 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        st.error("JSON 파일을 디코딩하는 데 실패했습니다.")
        return None

# 검색어와 일치하는 산업을 필터링하는 함수
def get_filtered_industries(json_file_path='industry_mapping.json', search_word=None):
    industry_mapping = load_json(json_file_path)
    if (industry_mapping is None) or (not industry_mapping):
        st.error("산업 매핑 데이터가 비어 있거나 로드할 수 없습니다.")
        return None

    filtered_industries = {}
    for industry, code in industry_mapping.items():
        documents = get_documents_by_industry_code("business_plan", code, search_word=search_word)
        if documents and (not search_word or any(search_word.lower() in doc.get('_source', {}).get('item_kw', '').lower() for doc in documents)):
            filtered_industries[industry] = code

    if not filtered_industries:
        st.error("검색된 단어를 포함하는 아이템이 있는 산업이 없습니다.")
        return None

    return filtered_industries

# 주어진 산업 코드와 검색어로 Elasticsearch에서 문서를 검색하는 함수
def get_documents_by_industry_code(index_name, industry_code, search_word=None):
    must_clauses = [{"term": {"ind_code.keyword": industry_code}}]
    should_clauses = []
    
    if search_word:
        should_clauses.append({"match": {"item_kw": search_word}})
    
    query = {
        "query": {
            "bool": {
                "must": must_clauses,
                "should": should_clauses
            }
        }
    }
    
    try:
        response = es.search(index=index_name, body=query, size=10000)
    except NotFoundError:
        st.error(f"인덱스 '{index_name}'를 찾을 수 없습니다.")
        return None
    except ConnectionError:
        st.error("Elasticsearch에 연결할 수 없습니다.")
        return None

    documents = [{"_id": hit["_id"], "_source": hit["_source"]} for hit in response["hits"]["hits"]]
    return documents

# 중첩된 데이터를 키를 통해 추출하는 함수
def get_nested_value(data, keys):
    for key in keys:
        if isinstance(data, list):
            try:
                key = int(key)
                data = data[key]
            except (ValueError, IndexError):
                return None
        elif isinstance(data, dict):
            data = data.get(key)
        else:
            return None
    return data

# 필드 이름을 번역하는 함수
def translate_field(key: str, field_mapping: dict) -> str:
    return field_mapping.get(key, key)

# 데이터를 테이블 형식으로 렌더링하는 함수
def render_table(data, field_mapping, title=None, highlight_word=None):
    if not data:
        return ""

    headers = set()
    rows = []

    # 데이터에서 필드 추출 및 번역
    for item in data:
        row = {}
        for key, value in item.items():
            headers.add(key)
            row[key] = value
        rows.append(row)

    # 헤더 정렬 및 추가
    def sort_key(header):
        if '고객 세그먼트 키워드' in header:
            return (0, header)
        elif '키워드' in header:
            return (1, header)
        elif '상세설명' in header:
            return (2, header)
        return (3, header)
    
    headers = sorted(headers, key=sort_key)
    
    # 중복 셀 합치기
    table = "<table style='width:100%; border-collapse: collapse;'>"
    table += "<tr>" + "".join(f"<th style='border: 1px solid #ddd; padding: 8px; text-align:left; font-weight: normal;'>{translate_field(header, field_mapping)}</th>" for header in headers) + "</tr>"
    
    previous_values = {header: None for header in headers}
    rowspan_counts = {header: 0 for header in headers}

    for row in rows:
        table += "<tr>"
        for header in headers:
            cell_value = row.get(header, '')
            cell_value_str = str(cell_value)  # 문자열로 변환
            if highlight_word and highlight_word.lower() in cell_value_str.lower():
                cell_value_str = cell_value_str.replace(highlight_word, f"<b><span style='color: #ff4b4b;'>{highlight_word}</span></b>")
            
            if cell_value == previous_values[header]:
                rowspan_counts[header] += 1
            else:
                if rowspan_counts[header] > 1:
                    table = table.replace(f"<td {header}>", f"<td rowspan='{rowspan_counts[header]}' {header}>", 1)
                rowspan_counts[header] = 1
            
            previous_values[header] = cell_value
            table += f"<td {header} style='border: 1px solid #ddd; padding: 8px; text-align:left; font-weight: normal;'>{cell_value_str}</td>"
        table += "</tr>"
    
    # 마지막 행의 rowspan 처리
    for header in headers:
        if rowspan_counts[header] > 1:
            table = table.replace(f"<td {header}>", f"<td rowspan='{rowspan_counts[header]}' {header}>", 1)

    table += "</table>"
    return table

def render_overview(data, field_mapping, highlight_word=None):
    overview_data = {
        "prod_serv_sum": get_nested_value(data, "overview.prod_serv_sum".split('.')),
        "motivation": {
            "reason": get_nested_value(data, "overview.motivation.reason".split('.')),
            "market_needs": get_nested_value(data, "overview.motivation.market_needs".split('.')),
            "vision": get_nested_value(data, "overview.motivation.vision".split('.'))
        },
        "uniq": get_nested_value(data, "overview.uniq".split('.')),
        "market_con": get_nested_value(data, "overview.market_con".split('.'))
    }

    st.markdown("#### Overview")
    
    for category, subcategories in overview_data.items():
        if category == "market_con" and subcategories:
            market_con_data = subcategories[0]
            years = list(market_con_data.keys())
            values = list(market_con_data.values())
            market_con_df = pd.DataFrame({'Year': years, 'Value': values}).set_index('Year')

            # Plotly를 사용한 그래프 생성
            fig = px.line(market_con_df, x=market_con_df.index, y='Value', 
                            title='시장 집중도',
                            labels={'Value': '집중도', 'Year': '연도'},
                            line_shape='linear', render_mode='svg')
            fig.update_layout(
                xaxis_title='연도',
                yaxis_title='HHI',
                template='plotly_white',
                hovermode='x unified',
                hoverlabel=dict(bgcolor="white", font_size=12),
                legend_title_text='',
            )
            # 라인 색상을 #ff4b4b로 설정
            fig.update_traces(line=dict(width=3, color='#ff4b4b'), hovertemplate='%{y}')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<div style='color: lightgrey; font-size: small;'>HHI (Herfindahl-Hirschman Index):<br>시장 집중도를 나타내는 지표로, 0에서 10,000 사이의 값을 가집니다.<br>값이 높을수록 시장 집중도가 높음을 의미합니다.</div>", unsafe_allow_html=True)

            continue
        
        if isinstance(subcategories, dict):
            st.markdown(f"##### {translate_field(category, field_mapping)}")
            for subcategory, value in subcategories.items():
                if value:
                    if highlight_word and highlight_word.lower() in value.lower():
                        value = value.replace(highlight_word, f"<b><span style='color: #ff4b4b;'>{highlight_word}</span></b>")
                    st.markdown(f"**{translate_field(subcategory, field_mapping)}**: {value}", unsafe_allow_html=True)
        elif isinstance(subcategories, list):
            st.markdown(f"##### {translate_field(category, field_mapping)}")
            uniq_kw_list = []
            uniq_desc_list = []
            for item in subcategories:
                uniq_kw = item.get("uniq_kw", "")
                uniq_desc = item.get("uniq_desc", "")
                if highlight_word:
                    uniq_kw = uniq_kw.replace(highlight_word, f"<b><span style='color: #ff4b4b;'>{highlight_word}</span></b>")
                    uniq_desc = uniq_desc.replace(highlight_word, f"<b><span style='color: #ff4b4b;'>{highlight_word}</span></b>")
                uniq_kw_list.append(uniq_kw)
                uniq_desc_list.append(uniq_desc)
            uniq_kw_str = ', '.join(uniq_kw_list)
            uniq_desc_str = '<br>'.join(uniq_desc_list)
            st.markdown(f"**{translate_field('uniq_kw', field_mapping)}**: {uniq_kw_str}", unsafe_allow_html=True)
            st.markdown(f"**{translate_field('uniq_desc', field_mapping)}**:<br>{uniq_desc_str}", unsafe_allow_html=True)
        else:
            if subcategories:
                value = subcategories
                if highlight_word and highlight_word.lower() in value.lower():
                    value = value.replace(highlight_word, f"<b><span style='color: #ff4b4b;'>{highlight_word}</span></b>")
                st.markdown(f"**{translate_field(category, field_mapping)}**: {value}", unsafe_allow_html=True)

# 특정 섹션을 렌더링하는 함수
def render_section(data, field, field_mapping, highlight_word=None):
    section_data = get_nested_value(data, field.split('.'))
    
    if section_data is None:
        st.write(f"{translate_field(field, field_mapping)}에 대한 데이터가 없습니다.")
        return

    if isinstance(section_data, list):
        table = render_table(section_data, field_mapping, title=field, highlight_word=highlight_word)
        st.markdown(table, unsafe_allow_html=True)
    elif isinstance(section_data, dict):
        render_overview(section_data, field_mapping, highlight_word=highlight_word)
    else:
        cell_value = section_data
        if highlight_word and highlight_word.lower() in cell_value.lower():
            cell_value = cell_value.replace(highlight_word, f"<b><span style='color: #ff4b4b;'>{highlight_word}</span></b>")
        st.markdown(f"{cell_value}", unsafe_allow_html=True)

# canvas_image 섹션을 렌더링하는 함수
def render_canvas_image(doc_id):
    index_name = "business_plan"

    # 추출하고자 하는 필드 목록과 경로
    fields = {
        "key_part_kw": ["business_canvas", "key_part", "key_part_kw"],
        "key_act_kw": ["business_canvas", "key_act", "key_act_kw"],
        "val_prop_kw": ["business_canvas", "val_prop", "val_prop_kw"],
        "cust_rel_kw": ["business_canvas", "cust_rel", "cust_rel_kw"],
        "cust_seg_kw": ["business_canvas", "cust_seg", "cust_seg_kw"],
        "key_res_kw": ["business_canvas", "key_res", "key_res_kw"],
        "chn_kw": ["business_canvas", "chn", "chn_kw"],
        "cost_str_kw": ["business_canvas", "cost_str", "cost_str_kw"],
        "rev_streams_kw": ["business_canvas", "rev_streams", "rev_streams_kw"]
    }

    # 빈 딕셔너리 생성
    data = {key: set() for key in fields}

    # 특정 문서 검색
    try:
        response = es.get(index=index_name, id=doc_id)

        # 문서에서 원하는 필드 값 추출
        source = response['_source']
        for key, path in fields.items():
            current = source
            try:
                for p in path:
                    if isinstance(current, list):
                        # 리스트의 모든 요소로 접근
                        for item in current:
                            current = item[p]
                            if isinstance(current, list):
                                data[key].update(current)
                            else:
                                data[key].add(current)
                    else:
                        current = current[p]
                if isinstance(current, list):
                    data[key].update(current)
                else:
                    data[key].add(current)
            except (KeyError, TypeError, IndexError) as e:
                logging.warning(f"Field {path} not found in document ID {doc_id}: {e}")
                continue

    except Exception as e:
        logging.error(f"Error: {e}")

    # set을 다시 list로 변환하여 중복 값을 제거한 후, '\n'으로 구분된 문자열로 변환
    final_data = {key: '\n'.join(value) for key, value in data.items()}

    # 이미지를 불러옵니다
    image_path = 'BMC.png'
    image = Image.open(image_path).convert("RGB")
    image = image.resize((3000, 2000), Image.LANCZOS)  # 이미지를 더 크게 리사이즈

    draw = ImageDraw.Draw(image)

    # 나눔고딕 폰트 설정 (다운로드한 폰트 파일의 경로를 지정합니다)
    font_path = 'C:/Users/MSI/Desktop/study/SW_CAMP/프로젝트/사업계획서/NanumGothic.ttf'  # 나눔고딕 폰트 파일의 경로로 수정하세요
    font = ImageFont.truetype(font_path, 35)  # 폰트 크기를 80으로 설정

    # 섹션별 위치 지정 (텍스트를 적절한 위치에 배치)
    positions = {
        "key_part_kw": (170, 280),  
        "key_act_kw": (695, 280),   
        "val_prop_kw": (1230, 280),  
        "cust_rel_kw": (1790, 280),  
        "cust_seg_kw": (2380, 280), 
        "key_res_kw": (695, 870),  
        "chn_kw": (1790, 870), 
        "cost_str_kw": (170, 1450),  
        "rev_streams_kw": (1540, 1450) 
    }

    # 텍스트 추가
    for section, text in final_data.items():
        position = positions[section]
        draw.text(position, text, fill="black", font=font)

    # 결과 이미지 보여주기
    st.image(image, caption='Business Model Canvas', use_column_width=True)

# 주어진 섹션의 데이터를 디스플레이하는 함수
def display_section(data, section, field_mapping, highlight_word=None):
    section_fields = {
        "overview": [
            "overview.prod_serv_sum",
            "overview.motivation.reason",
            "overview.motivation.market_needs",
            "overview.motivation.vision",
            "overview.uniq"
        ],
        "canvas_image": [],
        "business_canvas": [
            "business_canvas.cust_seg",
            "business_canvas.val_prop",
            "business_canvas.chn",
            "business_canvas.cust_rel",
            "business_canvas.rev_streams",
            "business_canvas.key_res",
            "business_canvas.key_act",
            "business_canvas.key_part",
            "business_canvas.cost_str"
        ],
        "business_plan": [
            "detail_desc"
        ]
    }

    if section == "overview":
        render_overview(data['_source'], field_mapping, highlight_word=highlight_word)
    elif section == "canvas_image":
        render_canvas_image(data['_id'])  # 문서의 ID를 전달
    elif section == "business_plan":
        render_section(data['_source'], "detail_desc", field_mapping, highlight_word=highlight_word)
    else:
        col1, col2, col3 = st.columns(3)
        selected_fields = []
        for i, field in enumerate(section_fields[section]):
            col = col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3
            if col.checkbox(translate_field(field, field_mapping), key=field):
                selected_fields.append(field)

        if selected_fields:
            for field in selected_fields:
                render_section(data['_source'], field, field_mapping, highlight_word=highlight_word)

# 검색어 입력 시 호출되는 콜백 함수
def search_callback():
    st.session_state['search_word'] = st.session_state['search_input']

def main():
    st.title("Business Plan")
    
    # 검색어 입력 필드
    search_word = st.sidebar.text_input("사업기획서 관련 단어를 입력해주세요", key='search_input', on_change=search_callback)
    
    if 'search_word' in st.session_state:
        search_word = st.session_state['search_word']
        filtered_industries = get_filtered_industries(search_word=search_word)
        
        if filtered_industries:
            if 'selected_industry' not in st.session_state:
                st.session_state['selected_industry'] = None
            selected_industry = st.sidebar.selectbox(
                "찾고자 하는 산업을 선택해주세요",
                list(filtered_industries.keys()),
                index=list(filtered_industries.keys()).index(st.session_state['selected_industry']) if st.session_state['selected_industry'] in filtered_industries else 0
            )
            st.session_state['selected_industry'] = selected_industry
            selected_code = filtered_industries[selected_industry]
            st.session_state["selected_industry_code"] = selected_code
            
            documents = get_documents_by_industry_code("business_plan", selected_code, search_word=search_word)
            if documents is None:
                return
            
            field_mapping = load_json('field_mapping.json')
            if field_mapping is None:
                return
            
            if documents:
                filtered_documents = [doc for doc in documents if search_word.lower() in doc['_source'].get('item_kw', '').lower()]
                if filtered_documents:
                    documents = filtered_documents

                if 'selected_item' not in st.session_state:
                    st.session_state['selected_item'] = None
                item_names = [doc['_source']['item_kw'] for doc in documents]
                selected_item = st.sidebar.selectbox(
                    "아이템을 선택해주세요",
                    item_names,
                    index=item_names.index(st.session_state['selected_item']) if st.session_state['selected_item'] in item_names else 0
                )
                st.session_state['selected_item'] = selected_item
                
                if selected_item:
                    selected_document = next(doc for doc in documents if doc['_source']['item_kw'] == selected_item)
                    
                    section = st.sidebar.radio(
                        "섹션을 선택해주세요",
                        ["overview", "canvas_image", "business_canvas", "business_plan"]
                    )
                    
                    display_section(selected_document, section, field_mapping, highlight_word=search_word)
            else:
                st.write("해당 산업 코드에 대한 문서가 없습니다.")

if __name__ == "__main__":
    main()
