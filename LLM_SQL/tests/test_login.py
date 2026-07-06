import json
import requests

# 1. JSON 파일 읽기
def load_case(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# 2. HTTP 요청 실행
def run_case(case):
    url = case["url"]
    method = case["method"]
    data = case["data"]

    if method.upper() == "POST":
        response = requests.post(url, data=data)
    else:
        response = requests.get(url, params=data)

    return response

# 3. 실행
case = load_case("dataset/login_success.json")

response = run_case(case)

print("STATUS CODE:", response.status_code)
print("RESPONSE:", response.text)