import requests
from access_token import access_token
import json


# company_id = '08d5f048fcb54d65939c874d87259212'
# template_id = '260fe8ffae6f4f329c3ff73f6ba2d818'
# template_id = 'f0362d450f2d417592df9cf311403764'
url = f'https://kr-api.eformsign.com/v2.0/api/documents'
token = access_token()
headers = {'Content-Type':'application/json'}
headers['Authorization'] = f'Bearer {token}'

body = {
        "document_ids": 
        [
            "b993f42f94574e88a803d76a1e409ff1"
        ]
}



# with open('./json/document_data copy.json', encoding = 'UTF-8' ) as data:
#     data = data.read().encode('UTF-8')
body = str(body).encode('UTF-8')
r = requests.delete(url=url,headers=headers,data=body).json()
print(r)

