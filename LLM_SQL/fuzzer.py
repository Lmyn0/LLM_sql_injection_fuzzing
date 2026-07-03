import uuid

def make_trace(param_name: str) -> str:
    """
    파라미터별 고유 trace 생성
    예: TRACE_id_8f3a2c
    """
    random_part = uuid.uuid4().hex[:6]
    return f"TRACE_{param_name}_{random_part}"


def fuzz_input(data: dict, target_param: str):
    """
    data 안의 target_param 값을 trace로 교체한다.
    """
    trace = make_trace(target_param)

    fuzzed_data = data.copy()
    fuzzed_data[target_param] = trace

    return fuzzed_data, trace