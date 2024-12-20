import requests
from access_token import access_token
import json
from pprint import pprint
from datetime import datetime
import time

# url = 'https://kr-api.eformsign.com/v2.0/api/list_document'
# doc_id = "2c10679dc9b34e0895af46042d24e449"
doc_id = "ecf8ead6493243218fd07868a0c0c5e1"
url = f'https://kr-api.eformsign.com/v2.0/api/documents/{doc_id}?include_fields=true&include_histories=true'
token = access_token()
headers = {'accept': 'application/json', 'Content-Type':'application/json'}
headers['Authorization'] = f'Bearer {token}'

# with open('./json/document_list.json', encoding = 'UTF-8' ) as data:
#     data = data.read().encode('UTF-8')
r = requests.get(url=url,headers=headers).json()
# print(json.dumps(r,indent=4))
pprint(r)





# python에서 json 데이터를 예쁘게 indent하는 방법
# https://www.techiedelight.com/ko/pretty-print-json-file-python/


# ID가 없을 경우 document_status에서 field 확인 불가