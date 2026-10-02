from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:62265/v1",
    api_key="foundry-local"
)

messages = [
    {"role": "user", "content": "My name is Suraj."},
    {"role": "assistant", "content": "Nice to meet you, Suraj!"},
    {"role": "user", "content": "What is my name?"}
]


response = client.chat.completions.create(
    model="qwen2.5-1.5b-instruct-generic-gpu",
   messages=messages 
)  

print(response.choices[0].message.content)