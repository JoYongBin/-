import requests # API 요청라이브러리 (설치 필요)
from access_token import access_token # Acess_token.py 파일에서 access_token 함수를 가져옵니다
import json


# url = 'https://www.gov-eformsign.com/Service/v2.0/api/members?mailOption=false' # CSAP 전용 URL  
url = f'https://kr-api.eformsign.com/v2.0/api/members?mailOption=false' # SaaS 전용 URL
token = access_token() # token이란 변수는 access_token 함수의 값을 저장합니다.
headers = {'Content-Type':'application/json'} # headers는 json 타입으로 받아옵니다.
headers['Authorization'] = f'Bearer {token}'  # headers는 Bearer token 값을 저장합니다.


data = {
    "account": {
        "id": "whdydqlsdl@naver.com", # 비밀번호 초기화 할 계정 ID
        "password": "password123!@",     # 비밀번호 초기화 할 패스워드
        "name": "홍길동",             # 비밀번호 초기화 할 이름
        "contact": {
            "tel": "",           
            "number": '',
            "country_number": "+82",
            # 'email': 'abcd19283746@naver.com'
        },
        "department": "",
        "position": "",
        "agreement": {
            "marketing": False
        },
        "role" : [],
    }
}
data = str(data).encode('UTF-8') # 데이터를 UTF-8 방식으로 인코딩(한글이 깨지는 오류 방지)
r = requests.post(url=url,headers=headers,data=data).json() # data와 headers 값으로 호출
print(r) # 실행한 화면을 출력합니다.