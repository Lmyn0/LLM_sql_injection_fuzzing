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

def parse_output(output, trace):
    var_map = {}
    trace_payloads = []

    for line in output.splitlines():
        line = line.strip()

        if not line or "=" not in line:
            continue

        left, right = line.split("=", 1)
        left = left.strip()
        right = right.strip()

        # 1. var_1, var_2 같은 후보 저장
        if left.lower().startswith("var_"):
            var_map[left] = right
            continue

        # 2. trace와 연결된 줄 찾기
        if left.lower() == trace.lower():
            if right in var_map:
                trace_payloads.append(var_map[right])
            else:
                trace_payloads.append(right)

    # 3. trace 매핑이 없으면 fallback: var 후보 전체 사용
    if not trace_payloads:
        trace_payloads = list(var_map.values())

    return trace_payloads

def build_final_sql(trace_sql, trace, payload):
    return trace_sql.replace(trace, payload)

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

    payloads = parse_output(llm_output, trace)

    print("\n[PAYLOADS]")
    print(payloads)

    for payload in payloads:
        final_sql = build_final_sql(sql, trace, payload)

        print("\n[FINAL SQL]")
        print(final_sql)

if __name__ == "__main__":
    main()