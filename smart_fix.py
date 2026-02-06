import pandas as pd
import re

def smart_repair(input_file, output_file):
    df = pd.read_csv(input_file)
    repaired_rows = []
    
    # Keywords that indicate a "Title" rather than a "Company"
    title_filters = ['HR', 'DIRECTOR', 'HEAD', 'VP', 'VICE', 'PRESIDENT', 'MANAGER', 'RECRUITMENT', 'CHIEF', 'AVP', 'SVP']
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    print("Fixing company names and cleaning emails...")

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
        
        # 3. Identify the Company
        # We look at all columns after the name to find the one that ISN'T a title or email
        company = "Unknown"
        for item in row_values[2:]:
            item_upper = item.upper()
            if '@' in item or any(word in item_upper for word in title_filters):
                continue
            if len(item) > 2 and not item.isdigit():
                company = item
                break

        if email and company != "Unknown":
            repaired_rows.append({'Name': name, 'Email': email, 'Company': company})

    new_df = pd.DataFrame(repaired_rows)
    new_df.to_csv(output_file, index=False)
    print(f"Success! {len(new_df)} clean rows saved to {output_file}")

smart_repair("raw_contacts.csv", "cleaned_contacts.csv")