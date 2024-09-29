from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import ollama

# OpenAI compatibility
import openai

model_name = "llama3.1:8b"  # 기본 모델

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

    messages = [{'role': 'system', 'content': "You are a Python coding assistant. Your role is to help users by providing clear, concise, and accurate Python code for their programming needs. You should break down complex problems, provide explanations where necessary, and ensure that the code follows best practices. Avoid overly technical jargon unless requested by the user. Your tone should be friendly, professional, and supportive. Provide examples when needed and encourage good coding habits such as adding comments and using meaningful variable names."},
                {'role': 'user', 'content': user_message}]
    assistant_message = {'role': 'assistant', 'content': ''}

    async for response in await client.chat(model=selected_model, messages=messages, stream=True):
        if response['done']:
            break
        assistant_message['content'] += response['message']['content']

    return {"response": assistant_message['content']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
