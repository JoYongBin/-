import requests
from access_token import access_token
import json



ID = '7dydqls7@forcs.com'
url = f'https://kr-api.eformsign.com/v2.0/api/accounts/{ID}'
token = access_token()
headers = {'accept': 'application/json', 'Content-Type':'application/json'}
headers['Authorization'] = f'Bearer {token}'


# with open('./json/document_data copy.json', encoding = 'UTF-8' ) as data:
#     data = data.read().encode('UTF-8')
data= {
    "account":  
    {
        "id": "7dydqls7@forcs.com",
            "name": "조용빈123",
            "contact": {
                "country_number" : "+82",
                "number": "",
                'email': ''
            },
            "password" : "password123!@#",       # 기존 비밀번호
            "new_password" : "dydqls9914@" # 바꿀 비밀번호
    }
}
data=str(data).encode('UTF-8')
r = requests.patch(url=url,headers=headers,data=data).json()
print(r)