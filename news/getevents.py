import os
import sys
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.utils import timezone

# Add the project directory to the Python path
project_dir = '/home/mel/Desktop/code-lab/api/elira_api'
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elira_api.settings')
django.setup()

from news.models import TechEvent

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
        tomorrow = datetime.today().date() + timedelta(days=1)
        time_str = date_txt[:8]
        date_string = f"{tomorrow.strftime('%A')}, {tomorrow.strftime('%b %d')}, {time_str}"
        date = datetime.strptime(date_string, '%A, %b %d, %I:%M %p')
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
        date=date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        location=item.get('location', ''),
        organiser=item.get('organiser', ''),
        format=item.get('format', []),
        themes=item.get('themes', [])
    )
    tech_events.append(tech_event)

TechEvent.objects.bulk_create(tech_events)

print(f"Today's TechEvent Objects Created: {len(tech_events)}")

print('***************** Events Fetch Ended *****************')
