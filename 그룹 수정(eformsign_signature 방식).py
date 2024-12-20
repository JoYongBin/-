import requests
from access_token import access_token
from pprint import pprint
# Group_List.py에서 함수명을 끌어오지 않고 자체 지정

# ------------------------- API Header ------------------------
token = access_token()
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
}

# API URL
group_url = 'https://kr-api.eformsign.com/v2.0/api/groups'       # 그룹 URL
department_url = 'https://kr-api.eformsign.com/v2.0/api/groups'  # 그룹 부서 URL

# ------------------------- 함수 정의 ------------------------

# 그룹 목록 가져오는 함수
def group_list():
    response = requests.get(url=group_url, headers=headers)
    if response.status_code == 200:
        group_data = response.json()
        return [{"name": group["name"], "id": group["id"]} for group in group_data.get('groups', [])]
    else:
        print(f"그룹 리스트를 가져오기 실패: {response.status_code}, {response.text}")
        return []

# 부서 목록 가져오는 함수
def department_list(group_id):
    url = f'{department_url}?group_id={group_id}'
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        department_data = response.json()
        return {
            department["name"]: department.get("members", [])
            for department in department_data.get("departments", [])
        }
    else:
        print(f"부서 목록을 가져오기 실패 {group_id}: {response.status_code}, {response.text}")
        return {}

# -------------------- 본문 -----------------------------

if __name__ == "__main__":
    # 그룹 목록 가져오기
    g_list = group_list()

    # 그룹별 부서 및 멤버 업데이트
    for group in g_list:
        group_id = group["id"]
        group_name = group["name"]

        # 부서별 멤버 가져오기
        d_list = department_list(group_id)

        # URL 및 요청 본문 생성
        url = f"https://kr-api.eformsign.com/v2.0/api/groups/{group_id}"
        body = {
            "group": {
                "name": group_name,
                "description": "설명 기입 필요",
                "members": d_list.get(group_name, [])  # 그룹 이름을 키로 사용
            }
        }

        # API 요청 보내기
        response = requests.patch(url=url, json=body, headers=headers)

        # 결과 출력
        if response.status_code == 200:
            print(f"그룹 '{group_name}' 업데이트 완료:")
            pprint(response.json())
        else:
            print(f"Error Updating Group '{group_name}': {response.status_code}")
            print(response.text)

# ------------------------ 출력 ----------------------------
# 그룹 및 부서 목록 확인을 위한 추가 출력
    print("\n수정한 그룹 목록:")
    pprint(group_list())