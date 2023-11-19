import openai;
import json, os,sys
from dotenv import load_dotenv
load_dotenv()
from litellm import completion
from mathpix import extract_text
import gradio as gr

# Mock candidate information
candidates = {
    "candidate1": {
        "name": "John Doe",
        "info": "Experienced software developer with a focus on machine learning."
    },
    "candidate2": {
        "name": "Jane Smith",
        "info": "Recent graduate with a strong background in data science."
    },
    # Add more candidates as needed
}

resume_location = 'resume_pdfs/1BXAuw6f1rDF05P734y_O7K8fYwgDVZvV.pdf'
resume_mmd = extract_text((resume_location))

def get_prompt(resume_mmd, chat_history, question):
    history = ''
    for user, bot in chat_history:
        history += 'User:\n' + user + '\nResponse:\n' + bot + ' '
    return ('Given the resmue of a candidate, the previous chat history, and a question, answer the question as if you are the candidate. Keep the answers short and to the point.\n'
    + 'Resume:\n\n' + resume_mmd + '\nEnd Resume\n'
    + 'Chat History:\n\n' + history + '\nEnd Chat History\n'
    + 'Question:\n\n' + question + '\nEnd Question\n')

def chatbot_interface(candidate_name):
    candidate = candidates.get(candidate_name, {})
    
    if not candidate:
        return "Candidate not found."
    
    candidate_info = candidate.get("info", "")
    
    def inference(message, history, model = 'gpt-3.5-turbo'):
        try:
            messages_litellm = [{"role": "user", "content": get_prompt(resume_mmd, history, message)}]
            partial_message = ""
            for chunk in completion(model=model,
                                            messages=messages_litellm,
                                            stream=True):
                if 'content' in chunk['choices'][0]['delta']:
                    partial_message += chunk['choices'][0]['delta']['content']
                yield partial_message
        except Exception as e:
            print("Exception encountered:", str(e))
            yield f"An Error occured please 'Clear' the error and try your question again"
    
    return gr.ChatInterface(
        inference,
        chatbot=gr.Chatbot(height=400),
        textbox=gr.Textbox(placeholder="Enter text here...", container=False, scale=5),
        description=f"""
        You are chatting with a resume.""",
        title="Chat with Resume",
        examples=["Introduce yourself."],
        retry_btn="Retry",
        undo_btn="Undo",
        clear_btn="Clear",
    )

def echo(message, history):
    return message

# Create Gradio app
iface = gr.Interface(
    fn=chatbot_interface,
    inputs=gr.Dropdown(choices=list(candidates.keys()), label="Select Candidate"),
    outputs=gr.ChatInterface(echo),
    live=True
)

# Launch Gradio app
iface.launch()