import pandas as pd
import re

def clean_hr_data(input_file, output_file):
    # Load the raw data
    df = pd.read_csv(input_file)
    
    # We'll create a new list for the cleaned data
    cleaned_rows = []

    # Regex pattern to find an email address
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    print("Cleaning data and extracting emails...")

    for index, row in df.iterrows():
        # Get the messy text from the Email column (usually index 2)
        # We convert to string to avoid errors with empty cells
        content = str(row.iloc[2]) 
        
        # Search for an email in that block of text
        found_email = re.search(email_pattern, content)
        
        if found_email:
            email = found_email.group(0).lower().strip()
            # Remove any trailing dots that sometimes get captured from the PDF
            email = email.rstrip('.')
            
            # Keep the HR name (index 1) and Company (index 3)
            cleaned_rows.append({
                'Name': str(row.iloc[1]).strip(),
                'Email': email,
                'Company': str(row.iloc[3]).strip()
            })

    # Save to a new, clean CSV
    clean_df = pd.DataFrame(cleaned_rows)
    clean_df.to_csv(output_file, index=False)
    print(f"Done! Cleaned {len(clean_df)} contacts. saved to {output_file}")

# Run the cleaner
clean_hr_data("raw_contacts.csv", "cleaned_contacts.csv")