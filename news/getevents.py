import os
import sys
import django
import requests
from bs4 import BeautifulSoup
import datetime

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

# ------------------------ Eventbrite ------------------------
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
    date = datetime.strptime(
        '2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S') if date_txt == '' else datetime.strptime(date_txt, "%a, %b %d, %I:%M %p")

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
        'title': title,
        'date': date,
        'location': location,
        'organiser': organiser,
        'link': link,
        'img': img
    })

eventbrite_no = len(events)
print(f"From EventBrite: {eventbrite_no}")

# # ------------------------ Meetup ------------------------
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
    date = datetime.strptime(
        '2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S') if date_txt == '' else datetime.strptime(date_txt, "%a, %b %d · %I:%M %p %Z"),

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
        'title': title,
        'date': date,
        'location': location,
        'organiser': organiser,
        'link': link,
        'img': img
    })

meetup_no = len(events) - eventbrite_no
print(f"From Meetup: {meetup_no}")

print(f"Event Items Collected {len(events)}")


# ----------- Step Three: Purge Yesterday's events ------------------

today = datetime.date.today()
news_pieces = TechEvent.objects.filter(date_created__lt=today)
num_deleted, _ = news_pieces.delete()

print(f"Yesterday's TechEvent Objects Deleted: {num_deleted}")

# ----------- Step Four: Add Today's events ------------------

tech_events = []

for item in events:
    tech_event = TechEvent(
        source=item.get('source', ''),
        source_img=item.get('source_img', ''),
        title=item.get('title', ''),
        link=item.get('link', ''),
        header_img=item.get('header_img', ''),
        publication=item.get('published', ''),
        tags=item.get('tags', []),
    )
    tech_events.append(tech_event)

TechEvent.objects.bulk_create(tech_events)

print(f"Today's TechEvent Objects Created: {len(news_pieces)}")

# TODO : Get GDSC Events
print('***************** Events Fetch Ended *****************')
