from litellm import embedding
import os


# print(help(embedding))

response = embedding('huggingface/microsoft/codebert-base', input=["good morning from litellm"])
# print(len(response['data'][0]["embeddingtext-embedding-ada-002"]))
print(int(response['usage']["total_tokens"]))