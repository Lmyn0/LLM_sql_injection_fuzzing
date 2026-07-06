from mutator import mutate
from detector import detect
import requests
import time
import json

URL = "http://localhost/fuzzing_test/login.php"


# 1. runner 기능
def send_request(payload):
    data = {
        "id": payload,
        "pw": "test"
    }

    response = requests.post(URL, data=data)
    return response.text


# 2. payload parsing
def parse_output(output):
    lines = output.split("\n")
    payloads = []

    for line in lines:
        if "=" in line:
            try:
                payload = line.split("=", 1)[1].strip()
                payloads.append(payload)
            except:
                pass
    return payloads

# 3. log 저장
def save_log(payload, response, decision):
    data = {
        "payload": payload,
        "response": response,
        "decision": decision
    }

    with open("fuzz_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
        
# 4. main loop
def main():

    base_input = """
id=admin
pw=admin1234
"""

    while True:
        print("\n[+] Running mutation...")

        # 1. mutate
        llm_output = mutate(base_input)
        print("\n[LLM OUTPUT]\n", llm_output)

        # 2. parse
        payloads = parse_output(llm_output)
        print("\n[+] Payloads:", payloads)

        for p in payloads:
            print("\n[+] Testing:", p)

            # 3. request
            response = send_request(p)
            print("[RESPONSE]", response)

            # 4. detect
            decision = detect(response)
            print("[DETECTOR]", decision)

            # 5. log
            save_log(p, response, decision)

        time.sleep(2)


if __name__ == "__main__":
    main()