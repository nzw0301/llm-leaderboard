"""
このスクリプトは、指定されたモデルとチャットテンプレートを使用して、チャットプロンプトを生成します。

使用方法:
$ python test_chat_template.py -m <model_id> -c <chat_template>

例:

# モデルIDとchat_templateが同じ場合
$ python scripts/test_chat_template.py -m "rinna/nekomata-7b-instruction"

# モデルIDと異なるchat_templateを使用する場合
$ python scripts/test_chat_template.py -m "rinna/nekomata-7b-instruction" -c "tokyotech-llm/Swallow-MS-v0.1"

引数:

- `-m` または `--model-id`: モデルのID。
# - `-c` または `--chat-template`: チャットテンプレートのID。省略した場合、モデルIDが使用されます。
"""

from argparse import ArgumentParser

from jinja2 import Template
from utils import get_tokenizer_config

parser = ArgumentParser()
parser.add_argument("-m", "--model-id", type=str, required=True)
parser.add_argument("-c", "--chat-template", type=str)

model_id = parser.parse_args().model_id
chat_template = parser.parse_args().chat_template
if chat_template is None:
    chat_template = model_id

tokenizer_config = get_tokenizer_config(model_id, chat_template)
chat_template = Template(tokenizer_config.get("chat_template"))

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant","content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"},
]

prompt = chat_template.render(messages=messages, add_generation_prompt=True, **tokenizer_config)

print(f"""\
------ BEGIN OF PROMPT ------
{prompt}
------- END OF PROMPT -------\
""")
