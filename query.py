import weaviate
from weaviate.classes.init import Auth
import os
from weaviate.classes.config import Configure
import json
from openai import OpenAI

openai_key = None
with open("key.txt", "r") as file:
    openai_key = file.read()
os.environ["OPENAI_APIKEY"] = openai_key


headers = {
    "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY"),
}

client = weaviate.connect_to_local(headers=headers)

NAME = "HarryPotterSorcererStone"

collection = client.collections.get(NAME)

if collection is None:
    print("Collection not found.")
    exit(1)

openai_client = OpenAI()


while True:
    query = input("Enter a query: ")
    if query.lower() == "exit":
        break
    if len(query) == 0:
        print("Empty query. Please enter a valid query.")
        continue
    try:
        response = collection.query.near_text(
            query=query,
            limit=5
        )
        if response is None:
            print("No response from the server.")
            continue
        # print(response)

        context_str = '\n'.join([f" chapter {obj.properties['chapter']} - {obj.properties['content']}" for obj in response.objects])
        instruction_prompt = f'''You are a helpful chatbot.
        Use only the following pieces of context to answer the question. Don't make up any new information:
        {context_str}
        '''

        response_ai = openai_client.responses.create(
            model="gpt-4.1",
            instructions=instruction_prompt,
            input=query,
        )

        print(response_ai.output_text)


    except Exception as e:
        print(f"An error occurred: {e}")
        continue