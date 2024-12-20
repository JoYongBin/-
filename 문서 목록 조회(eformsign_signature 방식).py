import requests
from access_token import access_token
import json
from pprint import pprint

# 삭제된 문서 목록을 조회하는 API URL
url = url = 'https://kr-api.eformsign.com/v2.0/api/list_document?include_fields=true'
token = access_token()
headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
headers['Authorization'] = f'Bearer {token}'

# 삭제된 문서 목록을 조회하기 위한 데이터 설정
data = {
    "type": "04",  # 삭제된 문서 목록
    "title_and_content": "(전략기획실)협회 홍보물품 신청서",  # 제목 및 내용에 포함
    "title": "",  # 제목 포함
    "content": "",  # 내용 포함
    "limit": "1000",  # 최대 문서 조회 개수
    "skip": "0"  # limit을 1000으로 하고, skip을 0으로 설정
}

# 요청 보내기
r = requests.post(url=url, json=data, headers=headers).json()

# 문서 목록 출력
pprint(r)

{'ErrorMessage': "You don't have Open API permission.", 'code': '4030034'}