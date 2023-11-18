import openai;
import json, os,sys
from dotenv import load_dotenv
load_dotenv()
from litellm import completion
from mathpix import extract_text
import gradio

def get_prompt(resume_mmd, chat_history, question):
    return ('Given the resmue of a candidate, the previous chat history, and a question, answer the question as if you are the candidate. Keep the answers short and to the point.\n'
    + 'Resume:\n\n' + resume_mmd + '\nEnd Resume\n'
    + 'Chat History:\n\n' + chat_history + '\nEnd Chat History\n'
    + 'Question:\n\n' + question + '\nEnd Question\n')

def chat_with_resume(model, resume_location):
    resume_mmd = extract_text(resume_location)
    chat_history = ''
    print('You are now chatting with the resume ' + resume_location + '. Type in your question or type QUIT to stop.')
    while True:
        print('User:')
        question = input()
        print('\n')
        if question.strip().upper() == 'QUIT':
            break
        prompt = get_prompt(resume_mmd, chat_history, question)
        messages = [{ 'content': prompt, 'role': 'user'}]
        response = completion(model = model, messages = messages)['choices'][0]['message']['content']
        print('Response:\n' + response + '\n\n')
        chat_history += 'User:\n' + question + '\nResponse:\n' + response

def inference(message, history):
    try:
        flattened_history = [item for sublist in history for item in sublist]
        full_message = " ".join(flattened_history + [message])
        messages_litellm = [{"role": "user", "content": full_message}] # litellm message format
        partial_message = ""
        for chunk in litellm.completion(model="huggingface/meta-llama/Llama-2-7b-chat-hf",
                                        api_base="x.x.x.x:xxxx",
                                        messages=messages_litellm,
                                        max_new_tokens=512,
                                        temperature=.7,
                                        top_k=100,
                                        top_p=.9,
                                        repetition_penalty=1.18,
                                        stream=True):
            partial_message += chunk['choices'][0]['delta']['content'] # extract text from streamed litellm chunks
            yield partial_message
    except Exception as e:
        print("Exception encountered:", str(e))
        yield f"An Error occured please 'Clear' the error and try your question again"
model = 'chat-bison'
resume_location = 'resume_pdfs/1BXAuw6f1rDF05P734y_O7K8fYwgDVZvV.pdf'
chat_with_resume(model, resume_location)