import weaviate
from weaviate.classes.init import Auth
import os
from weaviate.classes.config import Configure
import json


openai_key = None
with open("key.txt", "r") as file:
    openai_key = file.read()
os.environ["OPENAI_APIKEY"] = openai_key


headers = {
    "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY"),
}

client = weaviate.connect_to_local(headers=headers)

NAME = "HarryPotterSorcererStone"

if client.collections.exists(NAME) is False:
    client.collections.create(
        NAME,
        vectorizer_config=[
            Configure.NamedVectors.text2vec_openai(
                name="title_vector",
                source_properties=["chapter", "content"],
                model="text-embedding-3-large",
                dimensions=1024
            )
        ],
        # Additional parameters not shown
    )
    collection = client.collections.get(NAME)

    source_objects = []
    with open ("info.json", "r") as file:
        for line in file.readlines():
            if len(line) > 0:
                source_objects.append(json.loads(line))

    with collection.batch.fixed_size(batch_size=100) as batch:
        for src_obj in source_objects:
            # The model provider integration will automatically vectorize the object
            batch.add_object(
                properties={
                    "chapter": src_obj["chapter"],
                    "content": src_obj["content"],
                },
            )
            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                break

    failed_objects = collection.batch.failed_objects
    if failed_objects:
        print(f"Number of failed imports: {len(failed_objects)}")
        print(f"First failed object: {failed_objects[0]}")


collection = client.collections.get(NAME)
response = collection.query.near_text(
    query="A holiday film",  # The model provider integration will automatically vectorize the query
    limit=2
) 



client.close()