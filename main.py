import gspread
import os,random
from Candidate import JobCandidate
from dotenv import load_dotenv
from claude_compator import bubble_sort
from results import writeToSheets
sa = gspread.service_account(filename='service_creds.json')
sh = sa.open("Figma_swe")
from set_envs import set_envs
set_envs()
wks = sh.worksheet("Sheet1")
data = wks.get_all_values()


# Load environment variables from the .env file
load_dotenv()
# destination_path = os.path.join(os.getcwd(), id)
NotList=['sasad3@gatech.edu','saad.mufti@mit.edu']
candidates=[]
for i in range(1, 5):
    candid =JobCandidate(data[i])
    if candid.email not in NotList:
        candidates.append(candid)

random.shuffle(candidates)
sort_cand = bubble_sort(candidates)
for candidate in sort_cand:
    print(candidate.email)


# writeToSheets(candidates)


# for candidate in candidates:
#     print(candidate)
#     print()  # Print a blank line between candidates for better readability
    





