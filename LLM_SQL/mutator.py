from ollama import chat

def load_prompt():
    with open("prompts/mutator_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def mutate(input_text):
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

    return response["message"]["content"]