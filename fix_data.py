import pandas as pd
import re

def repair_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    repaired_rows = []
    
    # Common words found in the "Title" column that shouldn't be in the "Company" column
    title_keywords = ['HR', 'DIRECTOR', 'HEAD', 'VP', 'VICE', 'PRESIDENT', 'RECRUITMENT', 'MANAGER', 'CHIEF', 'OFFICER']
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    for _, row in df.iterrows():
        # Convert all columns to strings to search them
        row_str = [str(val) for val in row.values]
        
        # 1. Find Name (Usually the second column)
        name = row_str[1].strip()
        
        # 2. Find Email
        email = None
        for item in row_str:
            match = re.search(email_pattern, item)
            if match:
                email = match.group(0).lower().strip().rstrip('.')
                break
        
        # 3. Find Company (The column that is NOT a name, NOT an email, and NOT a title)
        company = "Unknown"
        # We look at columns 3 and 4 specifically where the PDF data usually lands
        potential_cols = [row_str[3], row_str[2]] 
        if len(row_str) > 4: potential_cols.append(row_str[4])

        for col in potential_cols:
            col_upper = col.upper()
            # If the column doesn't have an @ symbol and doesn't have title keywords, it's the company
            if '@' not in col and not any(k in col_upper for k in title_keywords) and len(col) > 2:
                company = col.strip()
                break

        if email and company != "Unknown":
            repaired_rows.append({'Name': name, 'Email': email, 'Company': company})

    new_df = pd.DataFrame(repaired_rows)
    new_df.to_csv(output_file, index=False)
    print(f"Repair Complete: {len(new_df)} rows ready.")

repair_csv("raw_contacts.csv", "cleaned_contacts.csv")