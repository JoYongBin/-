import requests     # 데이터 및 API 가져오는 라이브러리
import os       
import pandas as pd # 데이터 분석 및 처리 라이브러리 (설치 필요)
import base64       # 데이터를 Base64로 인코딩 및 디코딩 하기 위한 라이브러리
import hashlib      # 데이터를 암호화 및 무결성 검증 라이브러리
import binascii     # 이진법 데이터와 ASCII Code 문자열 간의 변화를 위한 라이브러리
from time import time # 시간 측정을 위한 라이브러리 (Access_token은 기간이 1시간이기 때문입니다)
from ecdsa import SigningKey, VerifyingKey, BadSignatureError # 서명을 하기 위한 라이브러리(설치 필요)
from ecdsa.util import sigencode_der, sigdecode_der  

# 주의 사항: Personal, Prepaid 요금제의 경우에는 API Key 발급이 되지 않기 때문에 확인 필요
# 주의 사항: 문서 관리자의 권한이 필요. 일반 멤버의 경우 문서 관리자 권한 및 다운, 열람 권한을 부여해야 함.

apikey = '64aed1e9-bcef-436f-99da-7333a5ca952f' #API Key (eformsign signatuer 방식)
secretkey = '3041020100301306072a8648ce3d020106082a8648ce3d03010704273025020101042033b44b635c8f4216c9eccca9c68367ee066369ada6825e3872b43a13a18a40f9' #eformsign signature 비밀 키
adminid = 'pouony@kfca.re.kr' #계정 이메일 ID
str_bytes = apikey.encode('utf-8')
str_base64 = base64.b64encode(str_bytes)
base64key = str_base64.decode('utf-8')


def access_token():
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
    return access_token


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
    token = access_token()
    print("Access Token:", token)
except Exception as e:
    print("An error occurred:", e)
    

access_token()