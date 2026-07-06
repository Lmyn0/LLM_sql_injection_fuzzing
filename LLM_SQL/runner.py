import requests
import json
from mutator import mutate
from fuzzer import fuzz_input
from detector import detect
from datetime import datetime

URL = "http://localhost/fuzzing_test/login.php"

TARGET_NAME = "login_safe"
URL = f"http://localhost/fuzzing_test/{TARGET_NAME}.php"

TARGET_PAYLOAD_COUNT = 20
MUTATION_ROUNDS = 10

EVALUATION_MODE = True
EVAL_LOG_FILE = f"eval_result_{TARGET_NAME}.jsonl"


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

def collect_payloads(sql, trace):
    all_payloads = []

    for round_idx in range(MUTATION_ROUNDS):
        print(f"\n[+] Sending trace + SQL to mutator... Round {round_idx + 1}/{MUTATION_ROUNDS}")

        llm_output = generate_mutation(sql, trace)

        print("\n[LLM OUTPUT]")
        print(llm_output)

        payloads = parse_output(llm_output, trace)

        for payload in payloads:
            if payload not in all_payloads:
                all_payloads.append(payload)

            if len(all_payloads) >= TARGET_PAYLOAD_COUNT:
                break

        print(f"[PAYLOAD COUNT] {len(all_payloads)}/{TARGET_PAYLOAD_COUNT}")

        if len(all_payloads) >= TARGET_PAYLOAD_COUNT:
            print("[+] Target payload count reached.")
            break

    return all_payloads

def save_log(payload, original_sql, final_sql, detector_result, db_result=None, reason=""):
    log_data = {
        "time": datetime.now().isoformat(),
        "payload": payload,
        "original_sql": original_sql,
        "final_sql": final_sql,
        "detector_result": detector_result,
        "db_result": db_result,
        "reason": reason
    }

    with open("fuzz_result_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")

def execute_payload(payload):
    data = {
        "id": payload,
        "pw": "bbb"
    }

    response = requests.post(URL, data=data)
    return response.text

def is_db_error(response_text):
    error_keywords = [
        "Fatal error",
        "mysqli_sql_exception",
        "SQL syntax",
        "You have an error in your SQL syntax",
        "MariaDB"
    ]

    return any(keyword in response_text for keyword in error_keywords)

def normalize_detector_result(decision):
    text = decision.strip().lower().replace(".", "")

    if text.startswith("true"):
        return True

    if text.startswith("false"):
        return False

    return None


def classify_db_result(response_text):
    """
    실제 DBMS 실행 결과를 기준으로 실제 문제가 발생했는지 판단한다.

    actual_positive = True
        - SQL 문법 오류 발생
        - 또는 로그인 성공처럼 원래 실패해야 할 요청이 성공한 경우

    actual_positive = False
        - SQL은 정상 실행됐지만 결과가 없는 경우
    """

    if is_db_error(response_text):
        return True, "DBMS_FATAL_ERROR"

    try:
        data = json.loads(response_text)

        if data.get("status") == "success":
            return True, "SUCCESS_RESPONSE"

        if data.get("status") == "fail":
            return False, "NORMAL_FAIL"

    except json.JSONDecodeError:
        return False, "UNKNOWN_RESPONSE"

    return False, "UNKNOWN_RESPONSE"


def classify_eval_result(detector_bool, actual_positive):
    if detector_bool is True and actual_positive is True:
        return "TP"

    if detector_bool is True and actual_positive is False:
        return "FP"

    if detector_bool is False and actual_positive is True:
        return "FN"

    if detector_bool is False and actual_positive is False:
        return "TN"

    return "UNKNOWN"


def save_eval_log(payload, original_sql, final_sql, detector_result, db_result, actual_label, eval_label):
    log_data = {
        "time": datetime.now().isoformat(),
        "target": TARGET_NAME,
        "payload": payload,
        "original_sql": original_sql,
        "final_sql": final_sql,
        "detector_result": detector_result,
        "db_result": db_result,
        "actual_label": actual_label,
        "eval_label": eval_label
    }

    with open(EVAL_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")

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

    payloads = collect_payloads(sql, trace)

    print("\n[PAYLOADS]")
    print(payloads)
    print(f"\n[TOTAL PAYLOAD COUNT] {len(payloads)}")

    for payload in payloads:
        final_sql = build_final_sql(sql, trace, payload)

        print("\n[FINAL SQL]")
        print(final_sql)

        decision = detect(sql, final_sql)

        print("[DETECTOR]") 
        print(decision)

        detector_bool = normalize_detector_result(decision)

        if EVALUATION_MODE:
            print("[EVAL MODE] Executing payload regardless of Detector result...")

            db_result = execute_payload(payload)

            print("[DBMS RESULT]")
            print(db_result)

            actual_positive, actual_label = classify_db_result(db_result)
            eval_label = classify_eval_result(detector_bool, actual_positive)

            print("[EVAL RESULT]")
            print(f"actual_label: {actual_label}")
            print(f"eval_label: {eval_label}")

            save_eval_log(
                payload=payload,
                original_sql=sql,
                final_sql=final_sql,
                detector_result=decision,
                db_result=db_result,
                actual_label=actual_label,
                eval_label=eval_label
            )

        else:
            normalized_decision = decision.strip().lower().replace(".", "")

            if normalized_decision == "true":
                print("[LOG] Detector returned True. Logging without DBMS execution.")

                save_log(
                    payload=payload,
                    original_sql=sql,
                    final_sql=final_sql,
                    detector_result=decision,
                    db_result=None,
                    reason="Detector predicted SQL injection or meaningful SQL context change"
                )

            else:
                print("[DBMS] Detector returned False. Executing payload through login.php...")

                db_result = execute_payload(payload)

                print("[DBMS RESULT]")
                print(db_result)

                if is_db_error(db_result):
                    print("[LOG] DBMS error detected. Logging result.")

                    save_log(
                        payload=payload,
                        original_sql=sql,
                        final_sql=final_sql,
                        detector_result=decision,
                        db_result=db_result,
                        reason="DBMS error occurred during query execution"
                    )
if __name__ == "__main__":
    main()