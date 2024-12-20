import requests
from access_token import access_token
import json
import pprint

company_id = 'a9437181923f4a428f31eaa3c5c70065'
url = f'https://kr-api.eformsign.com/v2.0/api/companies/{company_id}/use_status'
token = access_token()
headers = {'accept': 'application/json'}
headers['Authorization'] = f'Bearer {token}'

# with open('./document_data.json', encoding = 'UTF-8' ) as data:
    # data = data.read().encode('UTF-8')
r = requests.get(url=url,headers=headers).json()
print(r)
# templates = r['templates']
# temp_name_list = list()
# for ii in templates:
#     temp_name_list.append(ii['name'])
# # print(','.join(temp_name_list))
# # print(temp_name_list)
# for ii in r['templates']:
#     if ii['name'] ==  '헤헤':
#         pprint.pprint(ii)
    
    


# python에서 json 데이터를 예쁘게 indent하는 방법
# https://www.techiedelight.com/ko/pretty-print-json-file-python/