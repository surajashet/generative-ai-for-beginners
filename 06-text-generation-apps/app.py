from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:62265/v1",
    api_key="foundry-local"
)

prompt = """Show me 5 recipes for a dish with the following ingredients:
chicken, potatoes, and carrots.
Per recipe, list all the ingredients used"""

response = client.chat.completions.create(
    model="qwen2.5-1.5b-instruct-generic-gpu",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)