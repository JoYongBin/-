import requests
from access_token import access_token
import json
import pprint
import aspose.pdf as ap
import io
from base64 import b64decode

# url = 'https://kr-api.eformsign.com/v2.0/api/documents/9a584a39f4e9423aaa6accd776484838/download_files?file_type=document,audit_trail&file_name=ddd.pdf'
url = 'https://kr-api.eformsign.com/v2.0/api/documents/2bdccf2257ea42abb5a4e23d65360976/download_files?file_type=document&file_name=ddd.pdf'
token = access_token()
headers = {'accept': 'application/json'}
headers['Authorization'] = f'Bearer {token}'
r = requests.get(url=url,headers=headers).content
print(r)
f = open('C:/Users/forcs/Downloads/연세의료원/file.pdf', 'wb')
f.write(r)
f.close()


# print(r)
# python에서 json 데이터를 예쁘게 indent하는 방법
# https://www.techiedelight.com/ko/pretty-print-json-file-python/