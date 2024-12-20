import os
import re
import requests
import pandas as pd
import json
from access_token import access_token  # access_token.py에서 access_token() 가져옴.

# 토큰 발급
token = access_token()

# 엑셀 파일 경로
excel_file_path = 'C:/Downloads/(주)청오플랜트(24년도 11월 완료 문서)/document_list.xlsx'

# 엑셀 파일 경로가 없으면 디렉토리 생성
def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

# 엑셀로 문서 목록을 저장하는 함수
def save_document_list_to_excel(documents):
    ensure_directory_exists(excel_file_path)  # 디렉터리 확인 및 생성

    data = []
    for document in documents:
        if document['current_status']['status_type'] == '003':
            doc_id = document['id']
            name = document['document_name']
            file_name = f"{name}_{doc_id}.pdf"
            data.append([file_name, ''])  # 파일명과 다운로드 상태 (빈 칸)

    # 데이터프레임 생성
    df = pd.DataFrame(data, columns=['FileName', 'Downloaded'])
    df.to_excel(excel_file_path, index=False)
    print(f"문서 목록이 엑셀 파일로 저장되었습니다: {excel_file_path}")

# 파일 다운로드 후 엑셀에 다운로드 결과를 기록하는 함수
def update_excel_with_download_status(file_name, status):
    # 엑셀 파일 로드
    df = pd.read_excel(excel_file_path)

    # 파일명에 해당하는 행 찾기
    index = df.index[df['FileName'] == file_name].tolist()

    if index:
        # 해당 파일명 옆에 다운로드 상태를 'O'로 표시
        df.at[index[0], 'Downloaded'] = status
        print(f"엑셀 업데이트: {file_name} - {status}")

    # 엑셀 파일에 변경 사항 저장
    df.to_excel(excel_file_path, index=False)

# 문서 목록을 처리하는 함수
def document_list():
    global token
    url = 'https://kr-api.eformsign.com/v2.0/api/list_document?include_fields=true'
    
    headers = {
        'accept': 'application/json', 
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # JSON 형식의 데이터를 생성
    data = {
        "type": "03",  # 01: 진행 중,   02: 처리할,     03: 완료 문서,      04: 문서 목록                                   * 코드 번호 참조 *
        "title_and_content": "",  # 제목 및 내용에서 포함되는 단어 설정,
        "title": "",  # 제목
        "content": "",  # 내용
        "limit": "500",  # 최대 문서 다운로드 개수
        "skip": "0",  # 목록에서 문서를 건너뛰고 표시할 수
        "start_update_date": "1730419200000",  # 시작 시간              *주의 사항* : 날짜 단위를 너무 길게 잡으면 504 error(Server Timeout), 해당 시간은 GPT Timestamp in seconds 검색 참고.
        "end_update_date": "1733011199000"  # 종료 시간                 *주의 사항* : 날짜 단위를 너무 길게 잡으면 504 error(Server Timeout), 해당 시간은 GPT Timestamp in seconds 검색 참고.
    }

    # 요청을 보내고 응답을 받음
    r = requests.post(url=url, json=data, headers=headers)
    
    if r.status_code == 200:
        try:
            response_json = r.json()  # JSON으로 파싱
            documents = response_json.get('documents', [])
            
            # 문서 목록을 엑셀 파일로 저장
            save_document_list_to_excel(documents)
            
            # 문서 목록을 처리
            for document in documents:
                if document['current_status']['status_type'] == '003':
                    doc_id = document['id']
                    name = document['document_name']
                    file_name = f"{name}_{doc_id}.pdf"
                    
                    # PDF 다운로드 시도
                    result = pdf_download(doc_id, name)
                    
                    # 다운로드 성공 여부를 엑셀에 기록
                    status = 'O' if result else 'X'
                    update_excel_with_download_status(file_name, status)
        
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON response")
    else:
        print(f"Error: Received status code {r.status_code}")

def sanitize_filename(name):
    # 파일 이름에서 허용되지 않는 문자 제거 (예: :, /, \ 같은 문자 및 공백, 탭)
    name = re.sub(r'[\\/*?:"<>|]', '_', name)  # 비허용 문자 제거
    name = name.replace('\t', '').replace('\n', '').strip()  # 탭 및 줄바꿈 제거
    return name

# PDF 다운로드 함수
def pdf_download(doc_id, name):
    global token
    
    # 파일 저장 경로 설정
    directory = 'C:/Downloads/(주)청오플랜트(24년도 11월 완료 문서)/'
    
    # 디렉터리가 존재하지 않으면 생성
    ensure_directory_exists(directory)

    # 파일 이름을 허용되지 않는 문자 없이 깨끗하게
    clean_name = sanitize_filename(name)

    # 파일 경로
    file_path = f'{directory}{clean_name}_{doc_id}.pdf'
    
    # API 요청 URL
    url = f'https://kr-api.eformsign.com/v2.0/api/documents/{doc_id}/download_files?file_type=document&file_name={clean_name}_{doc_id}'
    
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # 파일 다운로드
    r = requests.get(url=url, headers=headers)
    
    # 파일이 정상적으로 다운로드되었을 경우에만 저장
    if r.status_code == 200 and r.content:
        with open(file_path, 'wb') as f:
            f.write(r.content)
        print(f"Downloaded: {file_path}")
        return True
    else:
        print(f"Error: Failed to download PDF. Status Code: {r.status_code}, Content: {len(r.content)} bytes")
        return False

# 문서 목록 함수 호출
document_list()
