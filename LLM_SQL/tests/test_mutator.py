from mutator import mutate

input_data = """
id=admin
pw=admin1234
"""

result = mutate(input_data)

print(result)