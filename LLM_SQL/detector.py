from ollama import chat

def load_prompt():
    with open("prompts/detector_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def detect(original_sql, final_sql):
    prompt = load_prompt()

    full_prompt = prompt + f"""

Original SQL:
{original_sql}

Final SQL:
{final_sql}

Response format:
True or False only.
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    )

    return response["message"]["content"].strip()