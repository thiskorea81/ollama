import ollama
import asyncio

async def run(model: str):
  client = ollama.AsyncClient()
  # Initialize conversation with a user query
  content = input("Send a message: ")
  # content = 'What is the flight time from New York (NYC) to Los Angeles (LAX)?'
  messages = [{'role': 'user', 'content': content}]

  # First API call: Send the query and function description to the model
  response = await client.chat(
    model=model,
    messages=messages
  )

  print(response['message']['content'])


# Run the async function
model = 'llama3.1:8b'
asyncio.run(run('llama3.1:8b'))