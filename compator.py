import openai;
import json, os,sys
from dotenv import load_dotenv
load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")
import openai; openai.api_key = "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"
from Candidate import JobCandidate


import litellm
from litellm import completion


import xml.etree.ElementTree as ET







def printc(obj, color="cyan"):
    color_code = {
        "black": "30", "red": "31", "green": "32", "yellow": "33",
        "blue": "34", "magenta": "35", "cyan": "36", "white": "37"
    }
    colored_text = f"\033[{color_code[color]}m{obj}\033[0m" if color in color_code else obj
    print(colored_text)



LLM=os.environ.get("COMPARATOR_LLM","chat-bison")
# LLM=os.environ.get("COMPARATOR_LLM","gpt-3.5-turbo-1106")
def getContent(candidateA, candidateB) -> str:
    return (
        "Given the following two candidates, choose between the two. Here is the rubric: "
        + get_rubric()
        + "Candidate A: "
        + "\nRESUME:\n" +candidateA.resume_text+"\nEND Resume\n"
        + "\nGITHUB:\n" +candidateA.github_text+"\nEND GITHUB\n"
        + " END OF Candidate A"
        + "\n\nCandidate B: "
        + "\nRESUME:\n" +candidateB.resume_text+"\nEND Resume\n"
        + "\nGITHUB:\n" +candidateB.github_text+"\nEND GITHUB\n"
        + " END OF Candidate B"

    )



def google_compare_resumes(content:str, nameA="", nameB=""):
    choice =0
    messages=[
        {"role": "user", "content": "You are an LLM recrutier who will choose between two candidates based on an provided rubric"},
        {"role": "user", "content":         
            """
            You are an LLM recrutier who will choose between two candidates based on an provided rubric,
            you will only use bullet point and broken english instead of proper english to be more concise
            """
        },
        {"role": "assistant", "content":         
            """
            I can assist you in evaluating two candidates based on a provided rubric. 
            Provide me with the rubric or the criteria you'd like to use for the evaluation, 
            and I'll help you assess the candidates accordingly and explain myself in less that 50 words
            """
        },
        {"role": "user", "content": content}
        ]

    response =completion(model=LLM, messages=messages,max_tokens=170,)
    printc(response["choices"][0]["message"],'red')

    messages=[
        {"role": "assistant","content":str(response["choices"][0]["message"])},
        {"role": "user","content":"okay so now with just a single token select A or B, <select>choice letter goes here</select>"}
    ]
    retries=3
    while retries >0:
        response =completion(model=LLM, messages=messages,max_tokens=5,temperature=0.01)
        # printc(response,'cyan')
        html=''.join(str(response["choices"][0]["message"]['content']).split())
        if "<select>" in html:
            xml_content = f'<root>{html}</root>'
            root = ET.fromstring(xml_content)
            select_element = root.find('select')
            letter = str(select_element.text)
        else:
            letter = str(html)[0]

        
        if letter == 'A':
            printc(nameA+" wins over "+nameB,"cyan")
            return -1
        elif letter == 'B':
            printc(nameB+" wins over "+nameA,"green")
            return 1

                
        retries-=1

    

    return choice
    

def compare_resumes(content:str, nameA="", nameB=""):
    retries = 3
    choice = 0

    while retries > 0:
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4-0613',
                messages=[
        {"role": "user", "content":         
            """
            You are an LLM recrutier who will choose between two candidates based on an provided rubric,
            you will only use bullet point and broken english instead of proper english to be more concise in your justification
            You will also provide args for selectCandidate
            """
        },
        {"role": "assistant", "content":         
            """
            I can assist you in evaluating two candidates based on a provided rubric. 
            Provide me with the rubric or the criteria you'd like to use for the evaluation, 
            and I'll help you assess the candidates accordingly and explain myself conscisely and will
            provide args for selectCandidate
            """
        },
        {"role": "user", "content": content}

                ],
                functions=[
                    {
                        "name": "selectCanidate",
                        "description": "choose between the two canidates",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "choice_num": {
                                    "type": "integer",
                                    "description": "1 for Candidate A is the best fit, 2 for Candidate B is the best fit",
                                    "required": ["choice_num"],
                                },
                                "justifcation": {
                                    "type": "string",
                                    "description": "justifcation for why you chose the candidate",
                                    "required": ["justifcation"],
                                },
                            }
                        },
                    }
                ],
                function_call="auto",
            )

            message = response["choices"][0]["message"]

            if message.get("function_call"):
                function_name = message["function_call"]["name"]
                function_args = json.loads(message["function_call"]["arguments"])
                choice = (int(function_args["choice_num"]))

                if function_name == "selectCanidate":
                    if choice == 1:
                        choice = -1
                        printc(nameA+" wins over "+nameB, "cyan")
                    elif choice == 2:
                        choice = 1
                        printc(nameB+" wins over "+nameA, "green")

                    printc(function_args["justifcation"], "yellow")

            break  # Break the loop if everything went well

        except Exception as e:
            printc("Error: " + str(e), "red")
            retries -= 1
            if retries == 0:
                printc("Maximum retries reached.", "red")
                return 0  # Or any other default value or error indicator

    return choice

    


def get_rubric():
    text = open("rubric.txt","r").read()
    return "\nRubric:\n" +str(text)+"\nEND Rubric\n"





def comp(candidateA:JobCandidate, candidateB:JobCandidate, rub_id:int=0 ) -> int:
    comp_table= json.load(open("comparisons.json","r"))
    tag= (candidateA.email+"#"+candidateB.email+"#"+str(rub_id))
    inv_tag= (candidateB.email+"#"+candidateA.email+"#"+str(rub_id))
    if tag in comp_table:
        if comp_table[tag]==1:
            printc(candidateA.name+" wins over "+candidateB.name,"magenta")
        elif comp_table[tag]==-1:
            printc(candidateB.name+" wins over "+candidateA.name,"magenta")

        return comp_table[tag]
    elif inv_tag in comp_table:
        if comp_table[inv_tag]==1:
            printc(candidateA.name+" wins over "+candidateB.name,"magenta")
        elif comp_table[inv_tag]==-1:
            printc(candidateB.name+" wins over "+candidateA.name,"magenta")
    else:
        choice = compare_resumes(getContent(candidateA, candidateB), candidateA.name, candidateB.name)   
        comp_table[tag]=choice
        comp_table[inv_tag]=choice*-1

        json.dump(comp_table, open("comparisons.json","w"))
        return choice


def compute_scores(candidates):
    scores = {candidate.email: 0 for candidate in candidates}
    for i, candidateA in enumerate(candidates):
        for candidateB in candidates[i+1:]:
            result = comp(candidateA, candidateB)
            scores[candidateA.email] += result
            scores[candidateB.email] -= result
    print(scores)
    return scores

def bubble_sort(candidates: list) -> list:
    scores = compute_scores(candidates)
    return sorted(candidates, key=lambda x: scores[x.email])