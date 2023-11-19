from typing import Optional
import gdown
import os
from datetime import datetime  # Importing the datetime class directly
from gh import getBasicReport
from mathpix import extract_text
from pathlib import Path 
class JobCandidate:
    def __init__(self, data: list):
        self.timestamp = datetime.strptime(data[0], "%m/%d/%Y %H:%M:%S")
        self.name = data[1]
        self.email = data[2]
        self.resume_link = data[3]
        self.resume_text= self.parse_resume()
        self.cover_letter = data[4]
        self.linkedin = data[5]
        self.github_link = data[6]
        self.github_text= self.parse_gh()
        self.personal_website_link = data[7]
        self.visa_sponsorship = data[8]
        self.disability_status = data[9]
        self.ethnic_background = data[10]
        self.gender = data[11]
        self.military_service = data[12]

    def __str__(self):
        return (f"Job Candidate: {self.name}\n"
                f"Applied on: {self.timestamp}\n"
                f"Email: {self.email}\n"
                f"Resume {self.resume_text}\n"
                f"Personal Website: {self.personal_website_link}\n"
                f"Visa Sponsorship: {self.visa_sponsorship}\n"
                f"Disability Status: {self.disability_status}\n"
                f"Ethnic Background: {self.ethnic_background}\n"
                f"Gender: {self.gender}\n"
                f"Military Service: {self.military_service}")

    def parse_resume(self):
        id = self.resume_link.split('=')[-1]
        pdf_dir = os.path.join(os.getcwd(), "resume_pdfs")
        mmd_dir = os.path.join(os.getcwd(), "resume_mmds")

        # Ensure the directories exist
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        if not os.path.exists(mmd_dir):
            os.makedirs(mmd_dir)

        pdf_path = os.path.join(pdf_dir, f"{self.email}.pdf")
        mmd_path = os.path.join(mmd_dir, f"{self.email}.pdf.mmd")

        try:
            # Check if the parsed text already exists
            if os.path.exists(mmd_path):
                with open(mmd_path, "r") as f:
                    return f.read()
            else:
                # Download the PDF
                gdown.download(id=id, quiet=True, use_cookies=False, output=pdf_path)
                
                # Check if the download was successful
                if os.path.exists(pdf_path):
                    t = extract_text(pdf_path)
                    preproccessed = t.replace(self.name, "applicant")
                    preprocessed = preproccessed.replace(self.name.split(" ")[0], "applicant")
                    return preprocessed
                else:
                    return "Failed to download the PDF."
        except Exception as e:
            return str(e)  



    def parse_gh(self):
        username = self.github_link.replace("https://github.com/", "").replace("github.com", "").replace("/", "")

        summary=""
        if username:
            file_path = Path(os.getcwd()) / "gh_cache" / f"{username}.md"
            if not file_path.exists():
                summary = str(getBasicReport(username))
                # Write the summary to the file
                file_path.write_text(summary)
            else:
                summary = open(file_path,"r").read()
            return summary
        else:
            return ""
    def parse_portfolio(self):
        pass

    

    
    
    
    def __lt__(self, other):
        if not isinstance(other, JobCandidate):
            return NotImplemented
        return self.timestamp < other.timestamp

    def __eq__(self, other):
        return False