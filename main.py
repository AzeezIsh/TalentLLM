import gspread
import os,random
from Candidate import JobCandidate
from dotenv import load_dotenv
from compator import bubble_sort
from results import writeToSheets
from resume_conversation import chat_with_candidate
sa = gspread.service_account(filename='service_creds.json')
sh = sa.open("Figma_swe")
load_dotenv()

wks = sh.worksheet("Sheet1")
data = wks.get_all_values()


# Load environment variables from the .env file
load_dotenv()
# destination_path = os.path.join(os.getcwd(), id)

candidates=[]

# os.environ['COMPARATOR_LLM']="chat-bison"
os.environ['COMPARATOR_LLM']="gpt-3.5-turbo-1106"
for i in range(1, 7):
    candid =JobCandidate(data[i])
    candidates.append(candid)

# random.shuffle(candidates)
sort_cand = bubble_sort(candidates)

writeToSheets(candidates)

for idx, candidate in enumerate(sort_cand):
    print(str(idx) + '. ' + candidate.email)

print('Select a candidate to chat with. Type in their index number. Type -1 if you dont want to chat.')
idx = int(input())
if idx != -1:
    selected_candidate = candidates[idx]
    chat_with_candidate(selected_candidate)

# for candidate in candidates:
#     print(candidate)
#     print()  # Print a blank line between candidates for better readability
    





