import requests
from access_token import access_token
import json

ID = 'whdydqlsdl@naver.com'                                           # 삭제할 멤버 계정 ID
url = f'https://kr-api.eformsign.com/v2.0/api/members/{ID}'           # 삭제 URL
# url = 'https://www.gov-eformsign.com/Service/v2.0/api/members/{ID}' # CSAP 전용 
token = access_token()                                                # token 정보
headers = {'accept': 'application/json', 'Content-Type':'application/json'} # header에서 정보 가져옴
headers['Authorization'] = f'Bearer {token}'



# data=str(data).encode('UTF-8')
r = requests.delete(url=url,headers=headers).json()
print(r) # 결과 출력, 200이면 성공적으로 해당 멤버 삭제 완료.