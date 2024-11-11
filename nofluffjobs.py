import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_job_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    job_title_element = soup.find('h1', class_='font-weight-bold')
    job_title = job_title_element.text.strip() if job_title_element else "Nie znaleziono tytułu"

    company_element = soup.find('a', id='postingCompanyUrl')
    company = company_element.text.strip() if company_element else "Nie znaleziono nazwy firmy"
    
    categories_elements = soup.find_all('a', attrs={'data-cy': 'JobOffer_Category'})
    categories = [a.text.strip() for a in categories_elements] if categories_elements else []

    seniority_element = soup.find('li', id='posting-seniority')
    try:
        seniority_icon = seniority_element.find('inline-icon', maticon='star_border_outline')
        seniority = seniority_element.text.strip() if seniority_icon else "Nie znaleziono"
    except AttributeError:
        seniority = "Nie znaleziono"
        time.sleep(5)

    posting_specs_element = soup.find('section', id='posting-specs')
    details = posting_specs_element.find_all('li', class_='detail') if posting_specs_element else []
    job_details = {}
    for detail in details:
        key_element = detail.find('h3', class_='tw-text-sm')
        value_element = detail.find('span')
        if key_element and value_element:
            key = key_element.text.strip(":")
            value = value_element.text.strip()
            job_details[key] = value

    requirements = {}
    for req_type in ['musts', 'nices']:
        section = soup.find('section', attrs={'branch': req_type})
        if section:
            items = [span.text.strip() for li in section.find_all('li') for span in li.find_all('span')]
            requirements[req_type] = items

    salary_element = soup.find('h4', class_='tw-mb-0')
    salary = salary_element.text.strip() if salary_element else "Nie ujawniono"

    benefits_perks_elements = soup.find_all('section', class_=['purple', 'success'])
    benefits_perks = {}
    for element in benefits_perks_elements:
        title = element.find('h2').text.strip()
        items = [li.text.strip() for li in element.find_all('li')]
        benefits_perks[title] = items

    return {
        'Stanowisko': job_title,
        'Firma': company,
        'Wynagrodzenie': salary,
        'Wymagania (Obowiązkowe)': requirements.get('musts', []),
        'Wymagania (Mile widziane)': requirements.get('nices', []),
        'Kategorie': categories,
        'Seniority': seniority,
        **job_details,
        **benefits_perks
    }

def main():
    base_url = 'https://nofluffjobs.com'
    url = f'{base_url}/pl/backend?criteria=category%3Dfrontend,fullstack,mobile,embedded,testing,devops,architecture,security,game-dev,data,sys-administrator,agile,product-management,project-manager,business-intelligence,business-analyst,ux,support,erp,other'
    
    driver = webdriver.Chrome()
    driver.get(url)

    all_job_details = []
    scraped_links = set()

    for i in range(3):
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[nfjloadmore]'))
            )
            button.click()
            time.sleep(3)
        except:
            continue

    while True:
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[nfjloadmore]'))
            )
            button.click()
            time.sleep(3)
        except:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    postings_lists = soup.find_all('nfj-postings-list', attrs={'listname': 'search'})
    postings_list = postings_lists[1]
    job_links = [a['href'] for a in postings_list.find_all('a', href=True)]
    job_links = job_links[1:]

    for link in job_links:
        if link not in scraped_links:
            job_url = f'{base_url}{link}'
            print(f'Scraping: {job_url}')
            job_details = scrape_job_details(job_url)
            all_job_details.append(job_details)
            scraped_links.add(link)

    driver.quit()

    fieldnames = set()
    for job in all_job_details:
        fieldnames.update(job.keys())

    with open('nofluff_jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for job in all_job_details:
            writer.writerow(job)

if __name__ == "__main__":
    main()
