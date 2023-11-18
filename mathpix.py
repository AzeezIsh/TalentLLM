

import requests
import time
import json
import os
from dotenv import load_dotenv
load_dotenv()

HEADERS = {
    'app_id': os.environ.get('MATHPIX_APP_ID', 'default_app_id'),
    'app_key': os.environ.get('MATHPIX_APP_KEY', 'default_app_key')
}



import os
import json
import requests
import time

def extract_text(file_path: str) -> str:
    print("Parsing resume")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
    file_name = os.path.basename(file_path)
    
    url1 = 'https://api.mathpix.com/v3/pdf'
    
    with open(file_path, 'rb') as file:
        files = {'file': file}
        data = {'options_json': json.dumps({
            "conversion_formats": {"md": True},
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True
        })}
        status_resp = requests.post(url1, headers=HEADERS, files=files, data=data)
        
    if status_resp.status_code != 200:
        raise Exception(f"Failed to upload PDF: {status_resp.text}")
        
    status_resp_data = status_resp.json()
    pdf_id = status_resp_data.get('pdf_id')
    
    if not pdf_id:
        raise Exception("Failed to retrieve PDF ID from response.")
    
    time.sleep(1)
    
    url2 = f'https://api.mathpix.com/v3/pdf/{pdf_id}'
    while True:
        challenge_resp = requests.get(url2, headers=HEADERS)
        challenge_resp_data = challenge_resp.json()
        if challenge_resp_data.get('status') == 'completed':
            break
        time.sleep(1)
    
    url3 = f'https://api.mathpix.com/v3/pdf/{pdf_id}.mmd'
    contents = requests.get(url3, headers=HEADERS)

    if contents.status_code != 200:
        raise Exception(f"Failed to download converted file: {contents.text}")
    
    open(os.path.join(os.getcwd(),"resume_mmds", (str(file_name)+'.mmd')),"w").write(contents.text)
    
    return contents.text
