from github import Github,Auth
from github.Repository import Repository
from typing import List
import requests
import os, json, datetime, re,sys
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv
load_dotenv()
import litellm
from litellm import completion
os.environ['AWS_ACCESS_KEY_ID']="AKIAWE73I2DYVFLFNLHS"
os.environ['AWS_REGION_NAME']="us-east-1"
os.environ['AWS_REGION']="us-east-1"
os.environ['AWS_SECRET_ACCESS_KEY']="r9Eqo6kg3rg0zHwK41N7IhfdiuWt4lCr68EYO6fv"
os.environ['PALM_API_KEY']='AIzaSyBr-t20IcF2T1xItAnlyYuQ50Ctu6Y0y4I'
os.environ["VERTEXAI_PROJECT"] = "data-axe-386317"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_creds.json'

def printc(obj, color="cyan"):
    color_code = {
        "black": "30", "red": "31", "green": "32", "yellow": "33",
        "blue": "34", "magenta": "35", "cyan": "36", "white": "37"
    }
    colored_text = f"\033[{color_code[color]}m{obj}\033[0m" if color in color_code else obj
    print(colored_text)


auth = Auth.Token(os.environ.get('GH_KEY', 'default'))
g = Github(auth=auth)


def remove_html_and_urls(markdown_text):
    no_html = re.sub(r'<[^>]+>', '', markdown_text)
    pattern_urls = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\'(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    no_html_no_urls = re.sub(pattern_urls, '', no_html)

    return no_html_no_urls




def getGithubPinned(username: str)-> List[str]:
    repos = []
    today = datetime.datetime.now()
    day_1 = today.replace(day=1)
    start_date, end_date  = day_1.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
    
    url = f"https://github.com/{username}?tab=overview&from={start_date}&to={end_date}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pinned_items = soup.find_all('div', class_='pinned-item-list-item-content')
        
        repos = []
        for item in pinned_items:
            repo_name = item.find('span', class_='repo').text.strip()
            repos.append(repo_name)
    else:
        print(f"Failed to get pinned repos for {username}")
        
    return repos




def get_repositories(username: str)->List[Repository]:
    user = g.get_user(username)
    all_repos = [repo for repo in user.get_repos()]
    repo_dict = {repo.name: repo for repo in all_repos}
    pinned_repo_names = getGithubPinned(username)
    pinned_repos = []
    for name in pinned_repo_names:
        if name in repo_dict:
            pinned_repos.append(repo_dict.pop(name))
    sorted_repos = sorted(repo_dict.values(), key=lambda x: x.stargazers_count, reverse=True)
    final_repo_list = pinned_repos + sorted_repos

    return final_repo_list




def getBasicReport(username: str):
    user_repos = get_repositories(username)[:8]
    summaries=[]


    for repo in user_repos:
        
        try:
            content = ""
            content+="\nNAME: "+str(repo.full_name)+"\nSTARS: "+str(repo.stargazers_count)+"\nReadme: \n"
            files = repo.get_contents("")
            md_files = [file for file in files if file.name.endswith('.md')]

    
            md_file_content = repo.get_contents(md_files[0].path).decoded_content.decode()

            content+= str(remove_html_and_urls(str(md_file_content)))



            messages=[
                {"role": "user", "content": "I want you to summarize this repository and summarize the skills gained with this repository  "},
                {"role": "assistant", "content":         
                    """
                    Sure, I can help with that! Please provide me with the details for the repo and I'll be able to summarize it and outline the skills that can be gained from it.
                    Additonally I will grade the techinal complexity with it. I will also greatly take into consideration the Number of stars. Furthermore I Will use broken english to ensure
                    my statements are as short and concise as possible
                    """
                },
                {"role": "user", "content": content}
                ]

            response =completion(model="anthropic.claude-instant-v1", messages=messages,max_tokens=150,temperature=1.0)
            summaries.append(response["choices"][0]["message"]['content'])

        except:
            continue


    # message = completion(model="anthropic.claude-instant-v1", messages=messages)

    return summaries







print(getBasicReport(username='taliu02'))


