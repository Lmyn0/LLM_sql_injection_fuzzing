from ollama import chat

def load_prompt():
    with open("prompts/detector_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def detect(input_text):
    prompt = load_prompt()

    full_prompt = prompt + "\n\nINPUT:\n" + input_text

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    )

    output = response["message"]["content"]
    
    try:
        return json.loads(output)
    except:
        return {
            "label": output,
            "raw": True
        }