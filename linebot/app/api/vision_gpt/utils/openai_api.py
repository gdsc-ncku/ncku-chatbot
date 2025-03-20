from openai import OpenAI


API_KEY = 'your gpt key'
model = 'gpt-4o-mini'

def openai_api(messages):
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print(openai_api("你知道王建民嗎？"))