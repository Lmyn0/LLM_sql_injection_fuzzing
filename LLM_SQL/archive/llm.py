from ollama import chat

def ask(model:str, prompt:str):
    response = chat(
        model="llama3.2",
        messages = [
            {
                "role": "user",
                "content": "mutator_prompt.txt에 있는 파일을 읽고 결과를 생성해줘"
            }
        ]
    )
    return response.message.content

result = ask("llama3.2", "content")
print(result)