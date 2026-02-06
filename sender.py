import smtplib
import time
import pandas as pd
from email.message import EmailMessage
import os

# --- CONFIGURATION ---
GMAIL_USER = 'satyamsaurav2803@gmail.com' 
GMAIL_PASS = 'xmqv stci wrsg xcji' 
RESUME_PATH = r'C:\Users\SATYAM SAURAV\Desktop\Coldmails\satyamupdcv.pdf' 
LOG_FILE = 'last_sent_index.txt'

def get_last_index():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return int(f.read().strip())
    return 2  # Start at index 2 (skipping the header and previous tests)

def save_last_index(index):
    with open(LOG_FILE, 'w') as f:
        f.write(str(index))

def send_ds_outreach():
    df = pd.read_csv('cleaned_contacts.csv')
    
    # 1. Automatic Batching
    start_idx = get_last_index()
    daily_limit = 35 # Staying safe within Gmail's limits
    end_idx = start_idx + daily_limit
    
    current_batch = df.iloc[start_idx:end_idx]
    
    if current_batch.empty:
        print("All contacts have been emailed!")
        return

    print(f"Resuming from index {start_idx}. Sending {len(current_batch)} emails...")

    last_successful_idx = start_idx

    for index, row in current_batch.iterrows():
        hr_name = str(row['Name']).split()[0]
        company = str(row['Company']).strip()
        target_email = row['Email']

        # 2. Prepare the Email Message
        msg = EmailMessage()
        msg['Subject'] = f"Data Science Role - Satyam Saurav | VIT | {company}"
        msg['From'] = GMAIL_USER
        msg['To'] = target_email

        body = (
            f"Hi {hr_name},\n\n"
            f"I am a final-year B.Tech student at VIT Vellore (2026 batch) and I'm reaching out "
            f"regarding Data Science opportunities at {company}[cite: 30].\n\n"
            f"During my internship at Mleaptech Mobley, I improved ML model accuracy by 15%[cite: 14]. "
            f"My portfolio includes a Real-Time Sign Language Translator (CNN-LSTM) and a "
            f"Monument Image Classifier with 95% accuracy[cite: 39, 44]. I also published "
            f"research in IEEE ICCAMS 2025 regarding CNN optimization[cite: 50].\n\n"
            f"I've attached my resume and would appreciate the chance to discuss how my technical "
            f"skills in Python and SQL can contribute to your team at {company}[cite: 23].\n\n"
            f"Best regards,\n"
            f"Satyam Saurav\n"
            f"LinkedIn: linkedin.com/in/satyamsaurav28\n"
            f"GitHub: github.com/maisatyamhoon"
        )
        msg.set_content(body)

        # 3. Attach CV
        try:
            with open(RESUME_PATH, 'rb') as f:
                file_data = f.read()
                msg.add_attachment(
                    file_data, 
                    maintype='application', 
                    subtype='pdf', 
                    filename='Satyam_Saurav_Data_Science_CV.pdf'
                )
        except FileNotFoundError:
            print(f"ERROR: Resume not found at {RESUME_PATH}")
            return

        # 4. Secure Send
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(GMAIL_USER, GMAIL_PASS)
                smtp.send_message(msg)
                print(f"[{index}] Successfully sent to {hr_name} at {company}")
                last_successful_idx = index + 1
        except Exception as e:
            print(f"[{index}] Failed to send to {target_email}: {e}")
            # If Gmail blocks us mid-batch, stop and save progress
            save_last_index(last_successful_idx)
            return

        # 5. Cooldown (120s) - Essential for account safety
        if index < current_batch.index[-1]:
            time.sleep(120)

    # Save progress after a successful batch
    save_last_index(last_successful_idx)
    print(f"\nBatch Complete! Next run will start from index {last_successful_idx}.")

if __name__ == "__main__":
    send_ds_outreach()