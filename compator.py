import openai;
import json, os,sys
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
from Candidate import JobCandidate
def printc(obj, color="cyan"):
    color_code = {
        "black": "30", "red": "31", "green": "32", "yellow": "33",
        "blue": "34", "magenta": "35", "cyan": "36", "white": "37"
    }
    colored_text = f"\033[{color_code[color]}m{obj}\033[0m" if color in color_code else obj
    print(colored_text)


LLM=os.environ.get("COMPARATOR_LLM","gpt-4-0613")
# LLM=os.environ.get("COMPARATOR_LLM","gpt-3.5-turbo-1106")
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



def compare_resumes(content:str, nameA="", nameB=""):
    choice =0
    response = openai.ChatCompletion.create(
        model=LLM,
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
                        "description": "justifcation for why you chose the candidate max 25 words",
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
        try:
            function_args = json.loads(message["function_call"]["arguments"])
            choice = (int(function_args["choice_num"]))
        except:
            printc("eroor","red")
            printc(message["function_call"],'red')

            return 1
        if function_name == "selectCanidate":

            if choice==1:
                printc(nameA+" wins over "+nameB,"cyan")
            elif choice==2:
                printc(nameB+" wins over "+nameA,"green")

            printc(function_args["justifcation"],"yellow")

    return choice
    

def get_rubric():
    text = open("rubric.txt","r").read()
    return "\nRubric:\n" +str(text)+"\nEND Rubric\n"





def comp(candidateA:JobCandidate, candidateB:JobCandidate, rub_id:int=0 ) -> int:
    comp_table= json.load(open("comparisons.json","r"))
    tag= (candidateA.email+"#"+candidateB.email+"#"+str(rub_id))
    inv_tag= (candidateB.email+"#"+candidateA.email+"#"+str(rub_id))
    if tag in comp_table:
        return comp_table[tag]
    elif inv_tag in comp_table:
        return comp_table[inv_tag] * -1
    else:
        choice = compare_resumes(getContent(candidateA.resume_text, candidateB.resume_text), candidateA.name, candidateB.name)   
        if choice == 1:
            choice = -1
        elif choice == 2:
            choice = 1
        comp_table[tag]=choice

        json.dump(comp_table, open("comparisons.json","w"))
        
        return choice


def bubble_sort(candidates: list) -> list:
    n = len(candidates)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if candidates[j].email == candidates[j+1].email:
                continue
            elif comp(candidates[j], candidates[j+1]) > 0:
                candidates[j], candidates[j+1] = candidates[j+1], candidates[j]
                swapped = True
        if not swapped:
            break


    return candidates

