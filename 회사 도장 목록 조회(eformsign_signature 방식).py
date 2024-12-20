import requests
from access_token import access_token
import json
from pprint import pprint



url = 'https://kr-api.eformsign.com/v2.0/api/company_stamp'
token = access_token()
headers = {'accept': 'application/json', 'Content-Type':'application/json'}
headers['Authorization'] = f'Bearer {token}'


r = requests.get(url=url,headers=headers).json()
pprint(r)

# ID가 없을 경우 document_status에서 field 확인 불가