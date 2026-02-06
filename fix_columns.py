import pandas as pd
import re

def repair_excel_data(input_file, output_file):
    # Load the raw data from your extraction
    df = pd.read_csv(input_file)
    repaired_rows = []
    
    # Keywords that identify a Job Title (the hurdles we want to skip or shift)
    title_keywords = ['HR', 'DIRECTOR', 'HEAD', 'VP', 'VICE', 'PRESIDENT', 'MANAGER', 'RECRUITMENT', 'CHIEF', 'AVP', 'SVP']
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    print("Scanning rows for correct Company names...")

    for _, row in df.iterrows():
        # Convert the row into a list of strings
        vals = [str(v).strip() for v in row.values if pd.notna(v)]
        
        if len(vals) < 2: continue

        name = vals[1] # Name is usually second 
        email = None
        company = "Unknown"

        # 1. Find the Email anywhere in the row
        for v in vals:
            match = re.search(email_pattern, v)
            if match:
                email = match.group(0).lower().rstrip('.')
                break
        
        # 2. Find the Company
        # We look for the first string that is NOT a name, NOT an email, and NOT a title
        for v in vals[2:]:
            v_upper = v.upper()
            if '@' in v: continue # Skip emails
            if any(k in v_upper for k in title_keywords): continue # Skip job titles
            if len(v) > 2 and not v.isdigit(): 
                company = v
                break

        if email and company != "Unknown":
            repaired_rows.append({'Name': name, 'Email': email, 'Company': company})

    # Save the repaired data
    new_df = pd.DataFrame(repaired_rows)
    new_df.to_csv(output_file, index=False)
    print(f"Repair Complete: {len(new_df)} clean rows saved to {output_file}")

repair_excel_data("raw_contacts.csv", "cleaned_contacts.csv")