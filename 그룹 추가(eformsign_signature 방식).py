import requests
from access_token import access_token
import pandas as pd

# API URL 및 헤더 설정
url = 'https://kr-api.eformsign.com/v2.0/api/groups'
headers = {'Content-Type': 'application/json'}
headers['Authorization'] = f'Bearer {access_token()}'  # Access Token 가져오기

# 데이터를 읽을 엑셀 파일 경로 지정
dataset2 = pd.read_excel('C:/Users/forcs/OneDrive/바탕 화면/업무/연동_api_2024.08.05/API/그룹 추가.xlsx', index_col=0) 

# 그룹 이름 추출
ob = set()
for idx, ser in dataset2.iterrows():
    ob.add(ser.iloc[2])  # 세 번째 열에서 그룹 이름 추출
print(f"그룹 개수: {len(ob)}")
print(f"그룹 목록: {ob}")

# 그룹 생성 API 요청
for group_name in ob:
    body = {
        "group": {
            "name": group_name,
            "description": "",
            "members": []
        }
    }
    # 요청 보내기
    response = requests.post(url=url, headers=headers, json=body)
    print(response.json())  # 응답 출력
