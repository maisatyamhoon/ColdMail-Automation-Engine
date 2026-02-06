import pandas as pd
import re

def rebuild_clean_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    rebuilt_rows = []
    
    # Hurdles: Keywords that identify a Job Role rather than a Company name
    role_keywords = ['HR', 'DIRECTOR', 'HEAD', 'VP', 'VICE', 'PRESIDENT', 'MANAGER', 'RECRUITMENT', 'CHIEF', 'AVP', 'SVP', 'LEAD']
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    print("Re-mapping columns: Hunting for missing Company names...")

    for _, row in df.iterrows():
        # Clean all values in the row and remove empty ones
        vals = [str(v).strip() for v in row.values if pd.notna(v) and str(v).strip() != ""]
        
        if len(vals) < 2: continue

        # 1. Name is usually the second value
        name = vals[1] if len(vals) > 1 else "Professional"
        
        # 2. Extract Email using Regex
        email = None
        for v in vals:
            match = re.search(email_pattern, v)
            if match:
                email = match.group(0).lower().rstrip('.')
                break
        
        # 3. Find the Company
        # We search from the end of the row backwards, as Company is often last
        company = "Unknown"
        for v in reversed(vals):
            v_upper = v.upper()
            # If it's not the email and doesn't contain a job role keyword, it's the company
            if '@' not in v and not any(k in v_upper for k in role_keywords) and len(v) > 2:
                company = v
                break

        if email and company != "Unknown":
            rebuilt_rows.append({
                'Name': name,
                'Email': email,
                'Company': company
            })

    # Save the new correctly ordered file
    new_df = pd.DataFrame(rebuilt_rows)
    new_df.to_csv(output_file, index=False)
    print(f"Success! {len(new_df)} contacts re-mapped and saved to {output_file}")

rebuild_clean_csv("raw_contacts.csv", "cleaned_contacts.csv")