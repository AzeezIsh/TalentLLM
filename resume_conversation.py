import openai;
import json, os,sys
from dotenv import load_dotenv
load_dotenv()
from litellm import completion
from mathpix import extract_text
import gradio

def get_prompt(candidate, chat_history, question):
    return ('Given the details of a candidate, the previous chat history, and a question, answer the question as if you are the candidate. Keep the answers short and to the point.\n'
    + 'Candidate Details:\n\n' + str(candidate) + '\nEnd Candidate Details\n'
    + 'Chat History:\n\n' + chat_history + '\nEnd Chat History\n'
    + 'Question:\n\n' + question + '\nEnd Question\n')

def chat_with_candidate(candidate, model = 'chat-bison'):
    chat_history = ''
    print('You are now chatting with ' + candidate.name + '. Type in your question or type QUIT to stop.')
    while True:
        print('User:')
        question = input()
        print()
        if question.strip().upper() == 'QUIT':
            break
        prompt = get_prompt(candidate, chat_history, question)
        messages = [{ 'content': prompt, 'role': 'user'}]
        response = completion(model = model, messages = messages)['choices'][0]['message']['content']
        print('Response:\n' + response + '\n')
        chat_history += 'User:\n' + question + '\nResponse:\n' + response