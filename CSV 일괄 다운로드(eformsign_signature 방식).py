import os
import requests
import pandas as pd
from datetime import datetime, timezone
import ast  # 문자열을 딕셔너리로 변환하는 데 사용
from access_token import access_token  # access_token.py에서 access_token() 가져옴.

# 토큰 발급              (Eformsign_signature 방식)
token = access_token()

# CSV 파일 경로(데이터 값을 엑셀 파일로 저장할 경로)
csv_file_path = 'C:/Downloads/몬즈컴퍼니/몬즈컴퍼니 24년도 데이터.csv'

# 디렉토리 확인 및 생성 함수
def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

# 상태 값을 변환하는 함수, 상태 값이 03이란 문자열로 받아오기 때문에 해당 값에 매핑되는 값을 변환
def map_status(status_code):
    status_mapping = {
        '003': '완료',
        '002': '처리중',
        '001': '진행중'
    }
    return status_mapping.get(status_code, '알 수 없음')  # 매핑되지 않은 상태는 "알 수 없음" , 즉 status_code가 04(문서 목록)은 알 수 없음으로 처리.

# 밀리초 단위 타임스탬프를 날짜로 변환하는 함수(해당 함수를 설정하지 않으면 날짜 값이 지수 표기법 형태로 반환)
def convert_timestamp_to_date(timestamp):
    try:
        if not timestamp or pd.isna(timestamp):  # 빈 값 처리
            return ''
        timestamp = float(timestamp)  # 지수 표기법 처리
        date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)  # 밀리초를 초로 변환
        return date.strftime("%Y-%m-%d %H:%M:%S")  # 문자열 형식(년도-월-달 시간:분:초) 형태로 변환
    except Exception as e: # 예외 상황(Error)
        print(f"타임스탬프 변환 오류 발생: {e}")
        return ''

# 발신자 및 처리자에서 'name'과 'id' 추출 함수
def extract_name_and_id(sender_data):
    try:
        # 발신자 데이터를 문자열에서 딕셔너리로 변환
        if isinstance(sender_data, str):
            sender_dict = ast.literal_eval(sender_data)  # 안전하게 문자열을 딕셔너리로 변환
        elif isinstance(sender_data, dict):
            sender_dict = sender_data  # 이미 딕셔너리인 경우 그대로 사용
        else:
            return {'name': '', 'id': ''}  # 예상치 못한 데이터 형식 처리

        # 'name'과 'id' 키를 추출하여 반환, 없으면 빈 문자열 반환
        return {
            'name': sender_dict.get('name', ''),
            'id': sender_dict.get('id', '')
        }
    except Exception as e:
        print(f"발신자/처리자 이름 및 ID 추출 중 오류 발생: {e}")
        return {'name': '', 'id': ''}

# 문서 목록을 CSV로 저장하는 함수
def save_document_list_to_csv(documents):
    ensure_directory_exists(csv_file_path)  # 디렉터리 확인 및 생성

    data = []
    for document in documents:
        status_code = document.get('current_status', {}).get('status_type', '')  # 상태 코드
        status = map_status(status_code)  # 상태 코드 변환

        if status_code in ['003', '002', '001']:  # 유효한 상태만 처리
            # 발신자 정보 추출
            creator = extract_name_and_id(document.get('creator', ''))
            # 처리자 정보 추출
            last_editor = extract_name_and_id(document.get('last_editor', {}))

            # 작성일과 처리일 변환
            created_date = convert_timestamp_to_date(document.get('created_date', ''))  # 작성일 변환
            updated_date = convert_timestamp_to_date(document.get('updated_date', ''))  # 처리일 변환

            # 데이터를 추가, 날짜에 작은 따옴표 추가
            data.append([
                status,  # 상태
                document.get('document_name', ''),  # 제목
                document.get('document_id', ''),  # 문서 ID
                document.get('current_status', {}).get('step_name', ''),  # 단계
                creator['name'],  # 발신자 이름
                creator['id'],    # 발신자 ID
                f"'{created_date}",  # 작성일 (텍스트로 저장)
                last_editor['name'],  # 최종 수신자 이름
                last_editor['id'],    # 최종 수신자 계정 ID, 만약 이메일로 보내는 것이 아닌 전화번호로 보낼 경우, 해당 값이 진수로 변환(해당 부분은 Colume 값을 가져오기 때문이다.)
                f"'{updated_date}"  # 처리일 (텍스트로 저장)
            ])

    # 데이터프레임 생성(Column 값 지정)
    df = pd.DataFrame(data, columns=[
        '상태', '제목', '문서 ID', '단계', '발신자 이름', '발신자 ID', '작성일', '처리자 이름', '처리자 ID', '처리일'
    ])

    # CSV 파일 저장
    try:
        df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        print(f"문서 목록이 CSV 파일로 저장되었습니다: {csv_file_path}")
    except Exception as e:
        print(f"CSV 파일 저장 중 오류 발생: {e}")

# 문서 목록을 처리하는 함수
def document_list():
    global token
    url = 'https://kr-api.eformsign.com/v2.0/api/list_document?include_fields=true'
    
    headers = {
        'accept': 'application/json', 
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # JSON 요청 데이터
    data = {
        "type": "03",       # 완료 문서(01 = 처리, 02 = 진행, 03 = 완료, 04 = 문서 목록)
        "limit": "1000",    # 최대 문서 개수(limit 값을 2000이상으로 줄 경우, 서버 타임 아웃이 발생)
        "skip": "0",        # 건너뛸 개수 ex) limit을 1000, skip을 20으로 하면 2페이지부터 다운로드 시작. (1p부터 시작하려면 = 0, 2p부터 시작하려면 = 20)
        "start_update_date": "1704067200000",   # 시작 시간 (밀리초 단위) 
        "end_update_date": "1735689599000"      # 종료 시간 (밀리초 단위)
    }

    # API 요청
    r = requests.post(url=url, json=data, headers=headers)
    
    if r.status_code == 200:
        try:
            response_json = r.json()  # JSON 응답 파싱
            documents = response_json.get('documents', [])
            
            # 문서 목록을 CSV로 저장
            save_document_list_to_csv(documents)
        
        except Exception as e:
            print(f"JSON 파싱 중 오류 발생: {e}")
    else:
        print(f"Error: Received status code {r.status_code}")

# 실행
document_list()
