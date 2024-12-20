import requests
from access_token import access_token
import json
from pprint import pprint


# url = 'https://kr-api.eformsign.com/v2.0/api/groups?include_member=true&include_field=true'
url = 'https://kr-api.eformsign.com/v2.0/api/groups'            # 그룹 리스트
department_url = 'https://kr-api.eformsign.com/v2.0/api/groups' # 그룹 부서 리스트

token = access_token()
headers = {'accept': 'application/json', 'Content-Type':'application/json'}
headers['Authorization'] = f'Bearer {token}'

# with open('./document_list.json', encoding = 'UTF-8' ) as data:
#     data = data.read().encode('UTF-8')

def group_list():
    r = requests.get(url=url,headers=headers).json()
    group_list = list()
    for ii in r['groups']:
        group_list.append({"name":ii["name"],"id": ii['id']})
    return group_list

# 부서 목록 가져오는 함수

def department_list(group_id):
    # 특정 그룹 ID에 따라 API 호출
    url = f'{department_url}?group_id={group_id}'
    response = requests.get(url=url, headers=headers)
    response_data = response.json()

        # 부서 정보 처리
    departments = []
    for department in response_data.get('departments', []):  # 'departments' 키 확인
        departments.append({"name": department["name"], "id": department["id"]})
    return departments

# 실행 
if __name__ == '__main__':
    # 그룹 목록 출력
    groups = group_list()
    print("그룹 목록:")
    for group in groups:
        print(f"- {group['name']} (ID: {group['id']})")

    # 각 그룹의 부서 목록 출력
    for group in groups:
        print(f"\n{group['name']} 그룹의 부서 목록:")
        departments = department_list(group['id'])
        for department in departments:
            print(f"  - {department['name']} (ID: {department['id']})")

print(group_list())
        
    


# python에서 json 데이터를 예쁘게 indent하는 방법
# https://www.techiedelight.com/ko/pretty-print-json-file-python/