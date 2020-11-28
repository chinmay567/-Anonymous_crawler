import pandas as pd
from bs4 import BeautifulSoup
import requests


def extract(page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
    URL = f"https://www.freshersworld.com/jobs/jobsearch/python-developer-jobs-for-be-btech-in-bangalore?{page}"
    r = requests.get(URL, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def Scraper(soup):
    divs = soup.find_all('div', class_='top_space')
    for div in divs:
        company_name = div.find('a').text
        Eligibility = div.find('span', class_='qualifications').text
        job_desc = div.find('span', {'class': 'desc'}).text.replace('\n', '')
        try:
            experience = div.find(
                'div', {'class': 'col-md-3 col-xs-3 col-lg-3 padding-none'}).text
        except:
            experience = ' '
        Location = div.find(
            'div', {'class': 'col-md-5 col-xs-5 col-lg-5 padding-none'}).text
        Last_date = div.find(
            'div', {'class': 'col-md-4 col-xs-4 col-lg-4 padding-none'}).text
        jobs = {
            'company_name': company_name,
            'Eligibility': Eligibility,
            'job_description': job_desc,
            'experience': experience,
            'location': Location,
            'Last_date': Last_date
        }
        job_list.append(jobs)
    return


job_list = []
for i in range(1, 41, 10):
    print(f'num of jobs are getting:{i}')
    c = extract(0)
    Scraper(c)
print(len(job_list))

dataframe = pd.DataFrame(job_list)
print(dataframe.head())
dataframe.to_json('jobs.csv')
