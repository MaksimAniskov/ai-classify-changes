from langchain_core.prompts import ChatPromptTemplate
import langchain_openai
import langchain_ollama
import json
import re
import sys
import typing
import yaml


def diff_file_by_file(file) -> typing.Generator[list[str], None, None]:
    chunk = []
    for line in file:
        if re.match(r"^diff --git", line):
            if chunk != []:
                yield chunk
                chunk = []
            continue
        chunk.append(line.rstrip("\n"))
    yield chunk


class ParsedDiff:
    def __init__(self):
        self.file_name: str = None
        self.added_lines: list[str] = []


def extract_added_lines(diff: list[str]) -> ParsedDiff:
    # Example 1 (File b.txt modified)
    #
    # [
    #   'index 286e0c1..9d875f6 100644',
    #   '--- a/b.txt',
    #   '+++ b/b.txt',
    #   '@@ -1 +1,3 @@',
    #   '+b 3',
    #   '+b line 2',
    #   '+'
    # ]

    result = ParsedDiff()
    i: int = 0
    while True:
        m = re.match(r"^\+\+\+ b\/(?P<file_name>.+)", diff[i])
        i += 1
        if m:
            result.file_name = m.group("file_name")
            break

    for l in diff[i:]:
        leading_char = l[0]
        if leading_char == "+":
            result.added_lines.append(l[1:])

    return result


config = yaml.safe_load(open("config.yaml", "r"))

if config["model"]["provider"] == "openai":
    chat_provider_class = langchain_openai.ChatOpenAI
elif config["model"]["provider"] == "ollama":
    chat_provider_class = langchain_ollama.ChatOllama
else:
    raise ValueError(f"Unknown model provider: {config['model']['provider']}")

chat_prompt_template = ChatPromptTemplate(
    map(lambda e: tuple(e), config["prompt_template"])
)

if "params" in config["model"]:
    args = dict(config["model"]["args"])
else:
    args = {}
args["model"] = config["model"]["model"]

llm = chat_provider_class(**args)

for single_file_diff in diff_file_by_file(sys.stdin):
    if single_file_diff == []:
        continue
    parsed_diff = extract_added_lines(single_file_diff)

    chat = chat_prompt_template.invoke(
        {
            "categories": ", ".join(config["categories"]),
            "code_snippet": "\n".join(parsed_diff.added_lines),
            "output_example": '{"Invokes REST API": true, "Consumes messages from Kafka topic": false}',
        }
    )
    response = llm.invoke(chat)

    classification_result = response.content
    m = re.match(r".*(?P<json>{.*}).*", response.content.replace("\n", ""))
    if m:
        classification_result = json.loads(m.group("json"))
    else:
        classification_result = {}

    detected_categories = []
    for category in classification_result:
        if (
            classification_result[category]
            and type(classification_result[category]) == bool
        ):
            detected_categories.append(category)
    print(parsed_diff.file_name, ", ".join(detected_categories))
