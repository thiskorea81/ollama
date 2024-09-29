from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import ollama

# OpenAI compatibility
import openai

model_name = "llama3.2:1b"

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = ollama.AsyncClient()

@app.post("/chat")
async def chat(request: Request):

    ''' openai compatitable
    openai.base_url = "http://localhost:11434/v1"
    openai.api_key = 'ollama'

    response = openai.chat.completions.create(
        model='llama3.1',
        messages='하늘은 왜 파랄까?',
    )
    print(response)
    '''

    data = await request.json()
    user_message = data.get("message")
    selected_model = data.get("model", model_name)  # 기본 모델은 llama3.1:8b

    messages = [{'role': 'system', 'content': "파이썬 코드를 작성해줘.라고 질문을 받으면 전문적인 프로그래머로서의 역할을 해줘."},
                {'role': 'user', 'content': user_message}]
    assistant_message = {'role': 'assistant', 'content': ''}

    async for response in await client.chat(model=model_name, messages=messages, stream=True):
        if response['done']:
            break
        assistant_message['content'] += response['message']['content']

    return {"response": assistant_message['content']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
