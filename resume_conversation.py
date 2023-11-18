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

model = 'chat-bison'
resume_location = 'resume_pdfs/1BXAuw6f1rDF05P734y_O7K8fYwgDVZvV.pdf'
chat_with_resume(model, resume_location)