import hashlib
import binascii

from ecdsa import VerifyingKey, BadSignatureError
from ecdsa.util import sigencode_der, sigdecode_der
from flask import request


# request에서 header와 body를 읽습니다.
# 1. get eformsign signature
# eformsignSignature는 request header에 담겨 있습니다.
eformsignSignature = request.headers['eformsign_signature']


# 2. get request body data
# eformsign signature 검증을 위해 body의 데이터를 String으로 변환 합니다.
data = request.json


# 3. publicKey 세팅
publicKeyHex = "이 곳에 발급받은 공개 키를 입력하세요"
publickey = VerifyingKey.from_der(binascii.unhexlify(publicKeyHex))


# 4. verify
try:
    if publickey.verify(eformsignSignature, data.encode('utf-8'), hashfunc=hashlib.sha256, sigdecode=sigdecode_der):
        print("verify success")
        # 이곳에 이벤트에 맞는 처리를 진행 합니다.
except BadSignatureError:
    print("verify fail")