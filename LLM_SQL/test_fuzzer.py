from fuzzer import fuzz_input

data = {
    "id": "admin",
    "pw": "bbb"
}

fuzzed_data, trace = fuzz_input(data, "id")

print("원본:", data)
print("fuzzed:", fuzzed_data)
print("trace:", trace)