from litellm import embedding
import os
from set_envs import set_envs
set_envs()

# print(help(embedding))

response = embedding('huggingface/microsoft/codebert-base', input=["good morning from litellm"])
# print(len(response['data'][0]["embeddingtext-embedding-ada-002"]))
print(int(response['usage']["total_tokens"]))