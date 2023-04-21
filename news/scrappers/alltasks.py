import os
import sys

# venv_dir = 'home/melfayne/.virtualenvs/elira-virtualenv'
# venv_python = os.path.join(venv_dir, 'bin', 'python3.10')
# sys.executable = venv_python

# # Add the project directory to the Python path
# project_dir = '/home/melfayne/elira_api'
# sys.path.append(project_dir)

# # Set the DJANGO_SETTINGS_MODULE environment variable
# os.environ['DJANGO_SETTINGS_MODULE'] = 'elira_api.settings'

# Add the project directory to the Python path
project_dir = '/home/mel/Desktop/code-lab/api/elira_api'
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elira_api.settings')
# Load Django Project
import django
django.setup()

import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.utils import timezone

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

from news.models import TechEvent
from news.models import NewsPiece
from news.models import TechJob


print('***************** Events Fetch Started *****************')

events = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# ----------- Step One: Get Events ------------------

# ------------------------ Eventbrite
eventbrite_url = 'https://www.eventbrite.com/d/kenya/tech-events/'
eventbrite_res = requests.get(eventbrite_url, headers=headers)
eventbrite_content = eventbrite_res.content
eventbrite_soup = BeautifulSoup(eventbrite_content, 'html.parser')
eventbrite_listings = eventbrite_soup.find_all(
    'div', {'class': 'search-event-card-wrapper'})

for listing in eventbrite_listings:
    link = listing.find(
        'a', {'class': 'eds-event-card-content__action-link'})['href']

    title = listing.find('div', {
                         'class': 'eds-event-card__formatted-name--is-clamped eds-event-card__formatted-name--is-clamped-three eds-text-weight--heavy'}).text

    date_txt = listing.find('div', {
        'class': 'eds-event-card-content__sub-title eds-text-color--primary-brand eds-l-pad-bot-1 eds-l-pad-top-2 eds-text-weight--heavy eds-text-bm'}).text

    if 'Tomorrow' in date_txt:
        # tomorrow = datetime.today().date() + timedelta(days=1)
        # time_str = date_txt[:8]
        # date_string = f"{tomorrow.strftime('%A')}, {tomorrow.strftime('%b %d')}, {time_str}"
        # date = datetime.strptime(date_string, '%A, %b %d, %I:%M %p')
        continue
    elif 'Today' in date_txt:
        today = datetime.today().date()
        time_str = date_txt[9:]
        date_string = f"{today.strftime('%A')}, {today.strftime('%b %d')}, {time_str}"
        date = datetime.strptime(date_string, '%A, %b %d, %I:%M %p')
    elif date_txt == '':
        date = datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    else:
        current_year = datetime.now().year
        date_txt = str(current_year) + ' ' + date_txt
        date = datetime.strptime(date_txt, "%Y %a, %b %d, %I:%M %p")

    location = listing.find(
        'div', {'data-subcontent-key': 'location'}).text

    img_elem = listing.find('img', {'class': 'eds-event-card-content__image'})
    img = img_elem['src'] if img_elem else 'https://drive.google.com/file/d/1TPcHicT_Q0zWjnh-8KfHJ7A2Uag8-8D5/view?usp=sharing'

    organiser_elem = listing.find(
        'div',  {'data-subcontent-key': 'organizerName'})
    organiser = organiser_elem.text if organiser_elem else ''

    events.append({
        'source': 'Eventbrite',
        'isOnline': False,
        'title': title.title(),
        'date': date,
        'location': location,
        'organiser': organiser,
        'link': link,
        'img': img
    })

eventbrite_no = len(events)
print(f"From EventBrite: {eventbrite_no}")

# ------------------------ Meetup
meetup_url = 'https://www.meetup.com/find/ke--nairobi/technology/'
meetup_res = requests.get(meetup_url, headers=headers)
meetup_content = meetup_res.content
meetup_soup = BeautifulSoup(meetup_content, 'html.parser')
meetup_listings = meetup_soup.find_all(
    'div',  {'data-element-name': 'categoryResults-eventCard'})

for listing in meetup_listings:
    link = listing.find(
        'a', class_='w-full inline cursor-pointer relative hover:no-underline')['href']

    img = listing.find('picture').find('img')['src']

    date_txt = listing.find(
        'div', class_='flex flex-col uppercase text-sm leading-5 tracking-tight text-darkGold font-medium pb-1 pt-1 line-clamp-1 lg:line-clamp-2').find('time').text

    if date_txt == '':
        date = datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    else:
        current_year = datetime.now().year
        date_txt = str(current_year) + ' ' + date_txt
        date = datetime.strptime(date_txt, "%Y %a, %b %d · %I:%M %p %Z")

    title = listing.find(
        'h2', class_='text-gray7 font-medium text-base pt-0 pb-1 line-clamp-3').text

    org_elem = listing.find(
        'p', class_='hidden md:line-clamp-1 text-gray6').text
    parts = org_elem.split(' • ')
    organiser = parts[0][11:]
    location = parts[1]

    online_elem = listing.find('div', {'data-testid': 'online-indicator'})
    isOnline = True if online_elem else False

    events.append({
        'source': 'Meetup',
        'isOnline': isOnline,
        'title': title.title(),
        'date': date,
        'location': location,
        'organiser': organiser,
        'link': link,
        'img': img
    })

meetup_no = len(events) - eventbrite_no
print(f"From Meetup: {meetup_no}")

# ------------------------ GDSC

print(f"Event Items Collected {len(events)}")

# ----------- Step Two: Tag Events ------------------

EVENT_FORMATS = {
    'Meetup': ['meetup', 'day', 'festival', 'fest', 'mondays', 'tuesdays', 'wednesdays', 'thursdays', 'fridays', 'saturdays'],
    'Info Session': ['forum', 'expo', 'info session', 'workshop'],
    'Conference': ['conference', 'summit'],
    'Hackathon': ['hackathon'],
    'Bootcamp': ['bootcamp'],
    'Networking': ['networking'],
    'Mentorship': ['mentorship']
}


def get_tech_format(title):
    title = title.replace("'", " ").replace(',', ' ').replace('.', ' ')
    keywords = [word for word in title.lower().split()]

    format_matches = []
    for format, format_keywords in EVENT_FORMATS.items():
        for keyword in keywords:
            if keyword in format_keywords:
                if format not in format_matches:
                    format_matches.append(format)

    return format_matches


EVENT_THEMES = {
    'AI': ['ai', 'ai/machine', 'machine', 'learning', 'recognition', 'artificial', 'bots', 'chatbot', 'sentiment', 'neural', 'vision', 'intelligence'],
    'DevOps': ['devops', 'api', 'testing', 'pipeline', 'git', 'debugging', 'deployment', 'netlify', 'docker', 'kubernetes'],
    'Mobile Dev': ['kotlin', 'flutter', 'native', 'ios', 'android', 'swift', 'xamarin'],
    'Web Dev': ['react', 'javascript', 'html', 'css', 'angular', 'next.js', 'tailwind', 'web', 'wordpress', 'elementor', 'php', 'django', 'flask'],
    'Programming': ['python', 'java', 'ruby','c++', 'rust', 'structures', 'javascript', 'json', 'scrum', 'agile', 'git', 'rest', 'springboot', 'api', 'trees', 'graph', 'arrays', 'binary', 'software'],
    'Cybersecurity': ['cybersecurity', 'cyber', 'hacking', 'phishing', 'breaches', 'encryption', 'authentication', 'firewalls', 'theft', 'vpn', 'security'],
    'Cloud Computing': ['computing', 'aws', 'azure', 'cloud', 'quantum', 'storage', 'migration', 'crowdsource', 'service'],
    'Internet of Things': ['iot', 'sensors'],
    'Blockchain': ['cryptocurrency', 'blockchain', 'crypto', 'bitcoin', 'Dogecoin', 'ethereum', 'solidity', 'coin', 'web3', 'decentralized', 'ledger', 'contracts', 'mining'],
    'Databases': ['database', 'postgresql', 'mongodb', 'sql', 'server', 'oracle', 'mysql'],
}


def get_tech_themes(title):
    title = title.replace("'", " ").replace(',', ' ').replace('.', ' ')
    keywords = [word for word in title.lower().split()]

    theme_matches = []
    for theme, theme_keywords in EVENT_THEMES.items():
        for keyword in keywords:
            if keyword in theme_keywords:
                if theme not in theme_matches:
                    theme_matches.append(theme)

    return theme_matches


# tag event items
for item in events:
    item['format'] = get_tech_format(item['title'])
    item['themes'] = get_tech_themes(item['title'])

print('All News Items Tagged!')

# ----------- Step Three: Purge Yesterday's events ------------------

now = timezone.now()
news_pieces = TechEvent.objects.filter(date_created__lt=now)
num_deleted, _ = news_pieces.delete()

print(f"Yesterday's TechEvent Objects Deleted: {num_deleted}")

# ----------- Step Four: Add Today's events ------------------

tech_events = []

for item in events:
    tech_event = TechEvent(
        source=item.get('source', ''),
        isOnline=item.get('isOnline', False),
        title=item.get('title', ''),
        link=item.get('link', ''),
        img=item.get('img', ''),
        date=item.get('date').strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        location=item.get('location', ''),
        organiser=item.get('organiser', ''),
        format=item.get('format', []),
        themes=item.get('themes', [])
    )
    tech_events.append(tech_event)

TechEvent.objects.bulk_create(tech_events)

print(f"Today's TechEvent Objects Created: {len(tech_events)}")

print('***************** Events Fetch Ended *****************')



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
    'Mobile Dev': ['mobile'],
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
        posted=item.get('posted').date(),
        description=item.get('description', ''),
        areas=item.get('areas', [])
    )
    tech_jobs.append(tech_event)

TechJob.objects.bulk_create(tech_jobs)

print(f"Today's TechJob Objects Created: {len(tech_jobs)}")

print('***************** Jobs Fetch Ended *****************')


print('***************** News Fetch Started *****************')

news = []

# ----------- Step One: Get News & Articles from RSS Feeds ------------------

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

sources = [
    {
        "name": "Engadget",
        "link": "https://www.engadget.com/rss.xml",
        "img": "https://drive.google.com/file/d/1LOS41-dqwA8wegqRKmTPAr5xhvaJtICI/view?usp=share_link"
    },
    {
        "name": "CNET",
        "link": "https://www.cnet.com/rss/news/",
        "img": "https://drive.google.com/file/d/1LPiNv5K6ANBIrlB7enVj1tZ6QY5-SEZS/view?usp=share_link",
    },
    {
        "name": "freecodecamp",
        "link": "https://www.freecodecamp.org/news/rss/",
        "img": "https://drive.google.com/file/d/1KsDC9j0vvREl2P9WEgDTz2T1M3_88n4f/view?usp=share_link",
    },
    {
        "name": "Wired AI",
        "link": "https://www.wired.com/feed/tag/ai/latest/rss",
        "img": "https://drive.google.com/file/d/1L3WD9hSNmx08YpAwFGPdAhG8z15TdUPm/view?usp=share_link",
    },
    {
        "name": "Wired",
        "link": "https://www.wired.com/feed/category/ideas/latest/rss",
        "img": "https://drive.google.com/file/d/1LD2szw8gzvTXp9X6SIhEbSzE3BpjQom_/view?usp=share_link",
    },
    {
        "name": "DZone",
        "link": "https://feeds.dzone.com/home",
        "img": "https://drive.google.com/file/d/1KyMA7PwRwbEkGCBBVIdzjG40afp9pXnk/view?usp=share_link",
    },
    {
        "name": "Techpoint Africa",
        "link": "https://techpoint.africa/feed/",
        "img": "https://drive.google.com/file/d/1LOHMy44Ia3X_9VaTxaddQ2obkcU3LTMg/view?usp=share_link",
    },
    {
        "name": "Disrupt Africa",
        "link": "https://disrupt-africa.com/feed/",
        "img": "https://drive.google.com/file/d/1L30by4Cb4iYaUNbdNUuxL4Kblu1mUiEh/view?usp=share_link",
    },
    {
        "name": "ITNews Africa",
        "link": "https://www.itnewsafrica.com/feed/",
        "img": "https://drive.google.com/file/d/1Kk_P5p46WI1w5ItikanbIzKkUD-cSDF-/view?usp=share_link",
    },
    {
        "name": "TechCabal",
        "link": "https://techcabal.com/feed/",
        "img": "https://drive.google.com/file/d/1L-OL96wWBSlxEYottNlSFcWneHEEAxWo/view?usp=share_link",
    },
    {
        "name": "TechCityng",
        "link": "https://techcityng.com/feed/",
        "img": "https://drive.google.com/file/d/1KqwRFq4-AArUx42JA66j65Xua6fR4SXF/view?usp=share_link",
    },
    {
        "name": "Apps Africa",
        "link": "https://www.appsafrica.com/feed/",
        "img": "https://drive.google.com/file/d/1KmluEeQQLNJK3OW43dC3As-NaLXmTbwS/view?usp=share_link",
    },
    {
        "name": "Medium",
        "link": "https://medium.com/feed/tag/technology",
        "img": "https://drive.google.com/file/d/1aZdF0GlOcQblVtU6QmetOwsn5DqZ2paB/view?usp=share_link",
    },
    {
        "name": "Dev Community",
        "link": "https://dev.to/feed/",
        "img": "https://drive.google.com/file/d/19LSLyJp_MPYctLC15Vz6U2Nl1PDqxkHs/view?usp=share_link",
    }
]


# Function to source images for rss feed entries with no media-content
def getImageUrl(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    images = soup.find_all("img")
    count = 0

    for image in images:
        if image.has_attr("src"):
            count += 1
            if count == round(len(images) / 4):
                return(image["src"])

# Fetch news from sources
for source in sources:
    feed = feedparser.parse(source['link'])
    for entry in feed.entries:
        news_item = {
            "source": source['name'],
            "source_img": source['img'],
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        }

        if('media_thumbnail' in entry):
            news_item["header_img"] = entry.media_thumbnail[0]['url']
        elif('media_content' in entry):
            news_item['header_img'] = entry.media_content[0]['url']
        else:
            news_item["header_img"] = getImageUrl(entry.link)

        news.append(news_item)

print(f"News Items Collected: {len(news)}")

# ----------- Step Two: Tag News & Articles ------------------

TECH_TAGS = {
    'Entertainment': ['netflix', 'spotify', 'streaming', 'stream', 'hbo', 'hulu', 'prime', 'disney+', 'tv+'],
    'Gaming': ['gaming', 'playstation', 'ps5', 'games', 'controllers', 'xbox', 'nintendo', 'unity', 'unreal', 'twitch'],
    'AI': ['ai', 'openai', 'chatgpt', 'faceio', 'recognition', 'chatgpt-4', 'gpt-4', 'artificial', 'bots', 'chatbot', 'sentiment', 'neural', 'vision'],
    'Data Science': ['data', 'analytics', 'jupyter', 'julia', 'r', 'datasets', 'sql', 'pandas', 'numpy', 'scikit'],
    'BigTech': ['amazon', 'meta', 'google', 'apple', 'facebook', 'twitter', 'tesla', 'microsoft', 'ibm', 'silicon valley', 'nvidia'],
    'Apps': ['kindle', 'bing', 'zoom', 'jumia', 'tiktok', 'instagram', 'snapchat', 'whatsapp', 'wechat', 'uber', 'lyft', 'youtube'],
    'Space': ['nasa', 'spacex', 'mars', 'moon', 'astronomy', 'astrophysics'],
    'DevOps': ['devops', 'api', 'testing', 'pipeline', 'git', 'debugging', 'deployment', 'netlify', 'docker', 'kubernetes', 'ansible'],
    'OS': ['windows', 'ios', 'os', 'ubuntu', 'command', 'gui', 'virtual', 'virtual box', 'batch'],
    'Mobile Dev': ['kotlin', 'flutter', 'native', 'ios', 'android', 'swift', 'xamarin'],
    'Web Dev': ['react', 'javascript', 'html', 'css', 'angular', 'next.js', 'tailwind', 'web', 'wordpress', 'php', 'django', 'flask'],
    'Programming': ['python', 'java', 'c++', 'rust', 'javascript', 'json', 'scrum', 'agile', 'git', 'rest', 'springboot', 'api', 'trees', 'graph', 'arrays', 'binary', 'software'],
    'Cybersecurity': ['cybersecurity', 'cyber', 'hacking', 'phishing', 'breaches', 'encryption', 'authentication', 'firewalls', 'theft', 'vpn', 'security'],
    'Events': ['wwdc', 'event', 'summit', 'application', 'i/o'],
    'Business & Finance': ['venture', 'capital', 'fintech', 'banking', 'startup', 'entrepreneurship', 'e-commerce', 'ecosystem', 'lawsuit', 'fund', 'payday', 'bank', 'bankruptcy'],
    'Databases': ['database', 'postgresql', 'mongodb', 'sql', 'server', 'oracle', 'mysql'],
    'Networking': ['hub', 'switch', 'router', 'modem', 'vpn', 'lan', 'wan', 'wi-fi', 'network'],
    'Cloud Computing': ['computing', 'aws', 'azure', 'cloud', 'storage', 'migration', 'crowdsource', 'service', 'quantum'],
    'Internet of Things': ['iot', 'smart', 'wearable', 'sensors'],
    'Gadgets': ['smartphone', 'wireless', 'laptop', 'watch', 'tablet', 'smartwatch', 'headphone', 'camera', '5g', 'wi-fi', 'bluetooth', 'samsung', 'asus', 'sony'],
    'Energy & Sustainability': ['renewable', 'energy', 'electric', 'vehicles', 'carbon', 'footprint', 'climate', 'sustainable'],
    'Blockchain': ['cryptocurrency', 'blockchain', 'crypto', 'bitcoin', 'Dogecoin', 'ethereum', 'solidity', 'coin', 'web3', 'decentralized', 'ledger', 'contracts', 'mining']
}

stop_words = set(stopwords.words('english'))

def get_tech_topics(title):
    title = title.replace("'", " ").replace(',', ' ').replace('.', ' ')
    keywords = [word for word in title.lower().split() if word not in stop_words]

    tech_matches = []
    for topic, topic_keywords in TECH_TAGS.items():
        for keyword in keywords:
            if keyword in topic_keywords:
                if topic not in tech_matches:
                    tech_matches.append(topic)

    return tech_matches

# tag news items
for item in news:
    item['tags'] = get_tech_topics(item['title'])

print('All News Items Tagged!')

# ----------- Step Three: Add Today's news pieces ------------------

news_pieces = []

for item in news:
    news_piece = NewsPiece(
        source=item.get('source', ''),
        source_img=item.get('source_img', ''),
        title=item.get('title', ''),
        link=item.get('link', ''),
        header_img=item.get('header_img', ''),
        publication=item.get('published', ''),
        tags=item.get('tags', []),
    )
    news_pieces.append(news_piece)

NewsPiece.objects.bulk_create(news_pieces)

print(f"NewsPiece Objects Created: {len(news_pieces)}")

print('***************** News Fetch Complete *****************')

