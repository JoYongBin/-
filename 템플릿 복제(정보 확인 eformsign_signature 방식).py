import requests
from access_token import access_token 
from access_token_target import access_token_target
import json
from pprint import pprint

# template_id = 'b9602ac1241d46a4865eb492b01221e2'
# template_id = 'f0362d450f2d417592df9cf311403764'
url = f'https://kr-api.eformsign.com/v2.0/api/forms/info' # 템플릿 정보 조회 URL


# 원본 계정 Access_token
original_token = access_token() 
headers = {'Content-Type':'application/json'}
headers['Authorization'] = f'Bearer {original_token}'


# 복제 계정 Access_token
clone_token = access_token_target()
headers = {'Content-Type': 'application/json'}
headers['Authorization'] = f'Bearer {clone_token}'


# with open('./json/forms_info.json', encoding = 'UTF-8' ) as data:
#     data = data.read().encode('UTF-8')
data={
    "type" : "api", # type : api로 지정
    "template_id" : "f747adb97c90415e8640846650279404" # 원본 템플릿 ID
}

data= str(data).encode('UTF-8')
r = requests.get(url=url,headers=headers,data=data).json()
    # print(json.dumps(r,indent=4))
pprint(r)

