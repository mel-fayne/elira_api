import os
import sys
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.utils import timezone

# Add the project directory to the Python path
# project_dir = '/home/mel/Desktop/code-lab/api/elira_api'
# sys.path.append(project_dir)

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elira_api.settings')
# django.setup()

# from news.models import TechJob

print('***************** Jobs Fetch Started *****************')

jobs = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# ----------- Step One: Get Events ------------------

page = 1 
while page <= 10:
    url = 'https://www.myjobmag.co.ke/search/jobs?q=intern--software--data--design--network--developer--cyber--database&currentpage=' + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    job_listings = soup.find_all('li', class_='job-list-li')

    for listing in job_listings:
        company_elm = listing.find('li', class_='job-logo')
        if company_elm != None:
            company_elm = company_elm.find('img')    
            company = company_elm['alt']

            job_logo = company_elm['src']
            job_logo = "https://www.myjobmag.co.ke" + job_logo

            title = listing.find('li', class_='mag-b').find('a').text

            link = "https://www.myjobmag.co.ke" + listing.find('li', class_='mag-b').find('a').get('href')

            description = listing.find('li', class_='job-desc').text

            date_elm = listing.find('li', {'id': 'job-date'})
            posted = datetime.strptime('2023-01-01', '%Y-%m-%d')
            if date_elm != None:
                date_txt = date_elm.text
                posted = datetime.strptime(date_txt + ' 2023', '%d %B %Y')
            print(posted)

            jobs.append({
                'source': 'MyJobMag',
                'company': company,
                'job_logo': job_logo,
                'title': title,
                'link': link,
                'posted': posted,
                'description': description.replace('&nbsp;', ' ').replace('\n', ' ').replace('\xa0', ' ')
            })
    
    page += 1

print(f"Job Items Collected {len(jobs)}")

print('***************** Events Fetch Ended *****************')