from PIL import Image, ImageDraw, ImageFont
from elasticsearch import Elasticsearch
import logging


#인증(아이디, 패스워드)


#elastic server 호출 및 인증


# 인덱스 이름 설정
index_name = 'business_plan'  # 실제 인덱스 이름으로 변경
doc_id = 'doc_3'  # 실제 문서 ID로 변경

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
final_data


# 이미지를 불러옵니다
image_path = 'BMC.png'
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# 나눔고딕 폰트 설정 (다운로드한 폰트 파일의 경로를 지정합니다)
font_path = 'NanumGothic.ttf'  # 나눔고딕 폰트 파일의 경로로 수정하세요
font = ImageFont.truetype(font_path, 30)  # 폰트 크기를 30로 설정


# 섹션별 위치 지정 (텍스트를 적절한 위치에 배치)
positions = {
    "key_part_kw": (125, 250),  
    "key_act_kw": (525, 250),   
    "val_prop_kw": (950, 250),  
    "cust_rel_kw": (1400, 250),  
    "cust_seg_kw": (1850, 250), 
    "key_res_kw": (525, 720),  
    "chn_kw": (1400, 720), 
    "cost_str_kw": (125, 1220),  
    "rev_streams_kw": (1200, 1220) 
}

# 텍스트 추가
for section, text in final_data.items():
    position = positions[section]
    draw.text(position, text, fill="black", font=font)


# 결과 이미지 보여주기
image.show()