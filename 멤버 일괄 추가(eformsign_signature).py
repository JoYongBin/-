import requests
from access_token import access_token
import json
import pandas as pd

# --------------------------------- 계정 관련 필요한 정보 데이터 불러오기 -------------------------


# dataset2 = pd.read_excel('./엑셀 파일/kt estate 전자서명 인사정보_231204.xlsx', index_col = 0)
dataset2 = pd.read_excel('C:/Users/forcs/Downloads/Member_all_invitation.xlsx', index_col = 0) # 데이터가 저장되어 있는 엑셀 파일 경로 (사용자마다 수정)


# --------------------------------- eformsign API 호출 시 필요한 headers 정보----------------

url = f'https://kr-api.eformsign.com/v2.0/api/members?mailOption=false'
token = access_token()
headers = {'Content-Type':'application/json'}
headers['Authorization'] = f'Bearer {token}'

# --------------------------------데이터 처리 후 api 호출------------------------------------

for idx,ser in dataset2.iterrows():
    
    body = {
    "account": {
        "id": ser['ID'],
        "password": ser['PW'],
        "name": ser['멤버명'],
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
        # "external_sso_info": {
        # "uuid": '01020633641',
        # "account_id": 'rhkwk3333@gmail.com',
        # "idp_name": "rsa_customSSO"}
    }
}
    body = str(body).encode('UTF-8')
    r = requests.post(url=url,headers=headers,data=body).json()
    print(r)