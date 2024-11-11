# NoFluffJobs Job offers Scraper

## Overview
This project is a web scraper that collects job postings from the NoFluffJobs website. It extracts information such as job titles, company names, salaries, requirements, categories, and benefits, saving the data into a CSV file.

## Features
- Extracts detailed job information from NoFluffJobs.
- Handles dynamic content using Selenium to click the "Load More" button.
- Saves data in a CSV format for further analysis.

## Prerequisites
Before running the scraper, ensure you have the following installed:

- Python 3.x
- Google Chrome
- ChromeDriver (compatible with your Chrome version)
- Python packages:
  - `requests`
  - `beautifulsoup4`
  - `selenium`

Install the required packages:

pip install requests beautifulsoup4 selenium

## Installation
    Clone the repository:
    ```bash
    git clone https://github.com/yourusername/nofluffjobs-scraper.git
    cd nofluffjobs-scraper

Download ChromeDriver:

Ensure ChromeDriver is installed and added to your system PATH.

Run the script:
    ```bash
    python scraper.py

## Output
The scraper saves the extracted job data to nofluff_jobs.csv with columns such as:

- Stanowisko (Job Title)
- Firma (Company)
- Wynagrodzenie (Salary)
- Wymagania (Obowiązkowe) (Must-have requirements)
- Wymagania (Mile widziane) (Nice-to-have requirements)
- Kategorie (Categories)
- Seniority (Seniority level)
- Additional job-specific details and benefits

## Example CSV Output

Stanowisko,Firma,Wynagrodzenie,Wymagania (Obowiązkowe),Wymagania (Mile widziane),Kategorie,Seniority
Backend Developer,TechCompany,12,000 - 15,000 PLN,"Python, Django",None,Backend,Mid