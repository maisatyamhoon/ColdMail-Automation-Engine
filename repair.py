import pandas as pd
import re

def smart_repair(input_file, output_file):
    df = pd.read_csv(input_file)
    repaired_rows = []
    
    # Keywords that indicate a "Title" column rather than a "Company" column
    title_filters = ['HR', 'DIRECTOR', 'HEAD', 'VP', 'VICE', 'PRESIDENT', 'MANAGER', 'RECRUITMENT', 'CHIEF']
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    print("Analyzing columns to separate Companies from Job Titles...")

    for _, row in df.iterrows():
        row_values = [str(val).strip() for val in row.values if pd.notna(val)]
        
        # 1. Name is typically in the second column
        name = row_values[1] if len(row_values) > 1 else "Applicant"
        
        # 2. Extract Email from the row
        email = None
        for item in row_values:
            match = re.search(email_pattern, item)
            if match:
                email = match.group(0).lower().rstrip('.')
                break
        
        # 3. Identify the Company (The column that is NOT an email and NOT a title)
        company = "Unknown"
        # We look at all columns after the name
        for item in row_values[2:]:
            item_upper = item.upper()
            # Skip if it's an email or contains a Title keyword
            if '@' in item or any(word in item_upper for word in title_filters):
                continue
            # If it's a reasonably long string and not a number, it's likely the company
            if len(item) > 2 and not item.isdigit():
                company = item
                break

        if email and company != "Unknown":
            repaired_rows.append({'Name': name, 'Email': email, 'Company': company})

    new_df = pd.DataFrame(repaired_rows)
    new_df.to_csv(output_file, index=False)
    print(f"Repair Complete: {len(new_df)} clean contacts saved to {output_file}")

smart_repair("raw_contacts.csv", "cleaned_contacts.csv")