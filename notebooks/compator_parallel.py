import openai;
import json, os, threading

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
from Candidate import JobCandidate

def getContent(resumeA: str, resumeB: str) -> str:
    return (
        "Given the following two SWE candidates, choose between the two. Here is the rubric: "
        + get_rubric()
        + "Candidate A: "
        + "\nRESUME:\n" +resumeA+"\nEND Resume\n"
        + " END OF Candidate A"
        + "\n\nCandidate B: "
        + "\nRESUME:\n" +resumeB+"\nEND Resume\n"
        + " END OF Candidate B"
    )



def compare_resumes(content:str):
    choice =0
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": content}],
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
        if function_name == "selectCanidate":
            choice = (int(function_args["choice_num"]))
            print(function_args["justifcation"])
            
    return choice
    

def get_rubric():
    text = open("rubric.txt","r").read()
    return "\nRubric:\n" +str(text)+"\nEND Rubric\n"




def comp_parallel(candidateA: JobCandidate, candidateB: JobCandidate, rub_id: int, comp_table: dict, lock: threading.Lock):
    tag = f"{candidateA.email}#{candidateB.email}#{rub_id}"
    if tag not in comp_table:
        choice = compare_resumes(getContent(candidateA.resume_text, candidateB.resume_text))   
        if choice == 1:
            choice = -1
        elif choice == 2:
            choice = 1

        with lock:
            comp_table[tag] = choice


def pre_compute_comparisons(candidates: list, rub_id: int = 0) -> dict:
    comp_table= json.load(open("comparisons.json","r"))
    lock = threading.Lock()
    threads = []

    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            thread = threading.Thread(target=comp_parallel, args=(candidates[i], candidates[j], rub_id, comp_table, lock))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    json.dump(comp_table, open("comparisons.json","w"))
    return comp_table

def bubble_sort(candidates: list, rub_id: int = 0) -> list:
    n = len(candidates)
    comp_table = pre_compute_comparisons(candidates, rub_id)
    for i in range(n):
        for j in range(n - i - 1):
            tag = f"{candidates[j].email}#{candidates[j + 1].email}#"+str(rub_id)
            if comp_table[tag] > 0:
                candidates[j], candidates[j + 1] = candidates[j + 1], candidates[j]
    return candidates
