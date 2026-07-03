import requests
from mutator import mutate
from fuzzer import fuzz_input
URL = "http://localhost/fuzzing_test/login.php"

def get_sql_with_trace():
    data = {
        "id": "admin",
        "pw": "bbb"
    }
    fuzzed_data, trace = fuzz_input(data, "id")
    response = requests.post(URL, data=fuzzed_data)

    try:
        result = response.json()
    except Exception:
        print("[ERROR] JSON 파싱 실패")
        print(response.text)
        return None, None

    print("[PHP RESPONSE]")
    print(result)

    return result.get("debug_sql"), trace

def generate_mutation(sql, trace):
    history = ""

    input_text = f"""
history:
{history}

trace:
{trace}

SQL:
{sql}
"""

    return mutate(input_text)

def parse_output(output):
    payloads = []

    for line in output.splitlines():
        if "=" in line:
            payload = line.split("=", 1)[1].strip()
            payloads.append(payload)

    return payloads

def send_payload(payload):
    data = {
        "id": payload,
        "pw": "bbb"
    }

    response = requests.post(URL, data=data)
    return response.text

def main():
    print("[+] Sending trace to login.php...")

    sql, trace = get_sql_with_trace()

    if sql is None:
        print("[ERROR] debug_sql을 가져오지 못했습니다.")
        return

    print("\n[TRACE SQL]")
    print(sql)

    print("\n[+] Sending trace + SQL to mutator...")

    llm_output = generate_mutation(sql, trace)

    print("\n[LLM OUTPUT]")
    print(llm_output)

if __name__ == "__main__":
    main()