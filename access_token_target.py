import requests
import os
import pandas as pd
import base64
import hashlib
import binascii
from time import time
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from ecdsa.util import sigencode_der, sigdecode_der

# 주의 사항: Personal, Prepaid 요금제의 경우에는 API Key 발급이 되지 않기 때문에 확인 필요
# 주의 사항: 문서 관리자의 권한이 필요. 일반 멤버의 경우 문서 관리자 권한 및 다운, 열람 권한을 부여해야 함.

#dataset2 = pd.read_excel('C:/Users/forcs/OneDrive/바탕 화면/info.xlsx', index_col = 0)
#for idx,ser in dataset2.iterrows():
#    if idx == '(주)포시에스(테스트)123':
#        apikey,secretkey,adminid = ser['APIKEY'],ser['SECRETKEY'],ser['ADMINID'] 


# 템플릿을 복제 받을 계정 API
apikey = 'db8aa5d0-35bb-483d-af35-8b30c32303b1' #API Key (eformsign signatuer 방식)
secretkey = '3041020100301306072a8648ce3d020106082a8648ce3d030107042730250201010420b7c84c01273fec1dc8f7786bb440fa2010b7a6119ff931c249a65bef3f1d93fd' #eformsign signature 비밀 키
adminid = 'mozodog123@gmail.com' #계정 이메일 ID
str_bytes = apikey.encode('utf-8')
str_base64 = base64.b64encode(str_bytes)
base64key = str_base64.decode('utf-8')


def access_token_target():
    global base64key,adminid
    Sign = sign()

    url = 'https://api.eformsign.com/v2.0/api_auth/access_token'               # 일반 계정으로 Access_token 실행 할 경우
    # url = 'https://www.gov-eformsign.com/Service/v2.0/api_auth/access_token' # CSAP 공공 계정으로 Access_token 실행 할 경우


    headers = {'accept': 'application/json', 
               'eformsign_signature': Sign['eformsign_signature'], 
               'Authorization' : f'Bearer {base64key}',
               'Content-Type':'application/json'
               }
    
    data = str({'execution_time' : str(Sign['execution_time']),'member_id': adminid})
    r = requests.post(url=url,headers=headers,data=data).json()
    #print(data,headers)
    access_token = r['oauth_token']['access_token']
    return access_token_target


def sign():
    global secretkey
    privateKeyHex = secretkey
    privateKey = SigningKey.from_der(binascii.unhexlify(privateKeyHex))

    # execution_time - 서버 현재 시간
    execution_time_int = int(time() * 1000)
    execution_time = str(execution_time_int)

    # eformsign_signature 생성
    eformsign_signature = privateKey.sign(execution_time.encode('utf-8'), hashfunc=hashlib.sha256, sigencode=sigencode_der)
    # 현재 시간 및 현재 시간 서명값
    return {"execution_time" :int(execution_time) , "eformsign_signature" : binascii.hexlify(eformsign_signature).decode('utf-8')}

# 함수 호출
try:
    token = access_token_target()
    print("Access Token:", token)
except Exception as e:
    print("An error occurred:", e)
    

access_token_target()

# 첨언
# data는 string 형식으로 보내야됨