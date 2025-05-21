import os
import json



code = None
with open("key.txt", "r") as file:
    code = file.read()



text = []

curr_chapter = None
with open("harrypotter.txt", "r", encoding="cp1252") as file:
    count = 0
    curr_line = ""
    for line in file.readlines():
        if "CHAPTER" in line:
            if len(curr_line) > 0:
                text.append(curr_line.strip())
            text.append({"chapter": curr_chapter, "content": curr_line.strip()})
            curr_chapter = line[line.find("CHAPTER"):].strip()
            curr_line = ""
            continue
        if count % 10 == 0:
            if len(curr_line) > 0:
                text.append({"chapter": curr_chapter, "content": curr_line.strip()})
            curr_line = ""
        else:
            curr_line += line.strip() + " "
        count += 1

text.pop(0)
text.pop(0)
if len(curr_line) > 0:
    text.append({"chapter": curr_chapter, "content": curr_line.strip()})

with open("info.json", "w") as file:
    for line in text:
        if isinstance(line, dict):
            file.write(json.dumps(line) + "\n")




# os.environ["OPENAI_API_KEY"] = code

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# response = client.responses.create(
#     model="gpt-4.1",
#     input="Write a one-sentence bedtime story about a unicorn."
# )

# print(response.output_text)