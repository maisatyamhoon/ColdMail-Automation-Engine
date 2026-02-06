import pdfplumber
import pandas as pd

# The exact name of your file
file_path = "Company Wise HR Contacts - HR Contacts 2.pdf"
all_rows = []

print("Starting extraction (No Java required)...")

with pdfplumber.open(file_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            # We skip the first row of each page if it's just headers
            # but keep it for the very first page to get column names
            if len(all_rows) == 0:
                all_rows.extend(table)
            else:
                all_rows.extend(table[1:]) 

# Create the DataFrame
df = pd.DataFrame(all_rows[1:], columns=all_rows[0])

# Save it
df.to_csv("raw_contacts.csv", index=False)
print(f"Success! Extracted {len(df)} rows to raw_contacts.csv")