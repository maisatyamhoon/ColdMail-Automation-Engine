Project Overview
This project is an end-to-end Python-based automation pipeline designed to streamline professional outreach. It handles the complete lifecycle of lead generation: from extracting unstructured data from complex PDF directories to cleaning, validating, and executing high-precision email campaigns.

Core Features
Unstructured Data Extraction: Utilizes pdfplumber to parse 1,822 raw contact entries from multi-column PDF tables.

Intelligent Data Repair: Implemented a "Shift-Correcting" algorithm using Python to re-align data columns where PDF parsers originally failed, ensuring company names are correctly matched to contacts.

Regex-Based Validation: Uses Regular Expressions (Regex) to extract, clean, and validate over 1,815 professional email addresses and names.

Automated SMTP Engine: Features a custom-built email dispatcher with secure SMTP-SSL integration for high-volume outreach.

Persistent Progress Tracking: Includes a batch-tracking system (last_sent_index.txt) to allow the pipeline to resume from the last successful transmission, preventing duplicate emails and managing daily quotas.

Technical Architecture
1. Extraction & ETL
The pipeline begins by converting unstructured PDF data into a raw CSV format. This stage handles the technical challenge of "column bleeding" where dense table data often merges into a single string.

2. Data Cleaning & Logic Repair
To solve the issue of job titles (e.g., "Associate Director HR") being misidentified as company names, a keyword-based filtration system was developed. This system scans each row, identifies the "hurdle" (the job role), and shifts the pointer to the actual company name.

3. Automated Outreach
The engine executes a personalized email sequence. It includes a built-in 120-second cooldown timer between sends to maintain account health and adhere to Gmail's security protocols.

Tech Stack
Language: Python 3.x

Libraries:

Pandas: For large-scale data manipulation and sharding.

pdfplumber: For table-based data extraction.

re: For complex string pattern matching and validation.

smtplib: For managing email transmission protocols.

Environment: Virtual Environments (venv) for dependency management.

Performance & Impact
Efficiency: Successfully processed 1,800+ HR contacts, reducing the outreach workload by approximately 90% compared to manual processing.

Reliability: Integrated fail-safes to skip invalid data entries automatically, maintaining a professional sender reputation.

Developer
Satyam Saurav Final Year B.Tech, VIT Vellore (2026 Batch)
