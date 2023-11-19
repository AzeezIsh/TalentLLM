import gspread
from Candidate import JobCandidate
from typing import List
# Authenticate with Google Sheets using a service account
sa = gspread.service_account(filename='service_creds.json')

def writeToSheets(candidates: List[JobCandidate]):
    sh = sa.open("Figma_swe")
    new_sheet_title = "Results"  # Change this to your desired sheet name

    # Check if the sheet already exists
    try:
        existing_wks = sh.worksheet(new_sheet_title)
    except gspread.exceptions.WorksheetNotFound:
        existing_wks = None

    # If the sheet exists, delete it
    if existing_wks:
        sh.del_worksheet(existing_wks)
    new_wks = sh.add_worksheet(title=new_sheet_title, rows="100", cols="10")  # Adjust rows and cols as needed

    data_to_write = [
        [ "Timestamp", "Name", "Email", "Resume Link", "Cover Letter", "LinkedIn", "GitHub", "Personal Website", "Visa Sponsorship", "Disability Status", "Ethnic Background", "Gender", "Military Service" ]

    ]

    for candidate in candidates:
        data_row = [
            candidate.timestamp.strftime("%m/%d/%Y %H:%M:%S"),
            candidate.name,
            candidate.email,
            candidate.resume_link,
            candidate.cover_letter,
            candidate.linkedin,
            candidate.github_link,
            candidate.personal_website_link,
            candidate.visa_sponsorship,
            candidate.disability_status,
            candidate.ethnic_background,
            candidate.gender,
            candidate.military_service
        ]
        data_to_write.append(data_row)

    new_wks.update('A1', data_to_write)

        
    print(f"Data written to '{new_sheet_title}' sheet.")








