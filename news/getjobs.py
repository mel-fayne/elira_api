import os
import sys
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils import timezone

# Add the project directory to the Python path
project_dir = '/home/mel/Desktop/code-lab/api/elira_api'
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elira_api.settings')
django.setup()

from news.models import TechJob

print('***************** Jobs Fetch Started *****************')

jobs = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# ----------- Step One: Get Events ------------------

page = 1 
while page <= 10:
    url = 'https://www.myjobmag.co.ke/search/jobs?q=intern--software--data--design--network--developer--cyber--database&currentpage=' + str(page)
    response = requests.get(url, headers=headers)
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

# ----------- Step Two: Tag Jobs ------------------

JOB_AREAS = {
    'Data & AI': ['data'],
    'Software': ['software', 'devops'],
    'Networking & Cloud': ['network', 'networking', 'cloud'],
    'Cyber Security': ['cyber', 'security'],
    'Database': ['database', 'sql'],
    'Intern': ['intern', 'assistant'],
    'Developer': ['developer', 'frontend', 'backend', 'stack'],
    'Design': ['design', 'designer', 'ui/ux', 'ui', 'ux'],
    'Web Dev': ['web'],
    'IT & Support': ['support', 'it', 'ict'],
    'Sales': ['sales', 'marketing']
}


def get_job_area(title):
    title = title.replace("-", " ").replace(",", " ").replace("-", " ")
    keywords = [word for word in title.lower().split()]

    area_matches = []
    for area, area_keywords in JOB_AREAS.items():
        for keyword in keywords:
            if keyword in area_keywords:
                if area not in area_matches:
                    area_matches.append(area)

    return area_matches

# tag job items
for item in jobs:
    item['areas'] = get_job_area(item['title'])

print('All Jobs Items Tagged!')


# ----------- Step Three: Purge Yesterday's events ------------------

now = timezone.now()
tech_jobs = TechJob.objects.filter(date_created__lt=now)
num_deleted, _ = tech_jobs.delete()

print(f"Yesterday's TechJob Objects Deleted: {num_deleted}")

# ----------- Step Four: Add Today's events ------------------

tech_jobs = []

for item in jobs:
    tech_event = TechJob(
        source=item.get('source', ''),
        company=item.get('company', ''),
        title=item.get('title', ''),
        link=item.get('link', ''),
        job_logo=item.get('job_logo', ''),
        posted=item.get('posted').strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        description=item.get('description', ''),
        areas=item.get('areas', [])
    )
    tech_jobs.append(tech_event)

TechJob.objects.bulk_create(tech_jobs)

print(f"Today's TechJob Objects Created: {len(tech_jobs)}")

print('***************** Events Fetch Ended *****************')