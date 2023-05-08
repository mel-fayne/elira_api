import os
import sys
import django
import feedparser
import requests
from bs4 import BeautifulSoup

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Add the project directory to the Python path
project_dir = '/home/mel/Desktop/code-lab/api/elira_api'
sys.path.append(project_dir)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elira_api.settings')
django.setup()

from news.models import NewsPiece


print('***************** News Fetch Started *****************')

# ----------- Step One: Get News & Articles from RSS Feeds ------------------
news = []
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
    response = requests.get(url, headers=HEADERS)
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
    'Blockchain': ['cryptocurrency', 'blockchain', 'crypto', 'bitcoin', 'Dogecoin', 'ethereum', 'solidity', 'coin', 'web3', 'decentralized', 'ledger', 'contracts', 'mining'],
    'Design': ['design', 'ui', 'ux', 'graphics']
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

# ----------- Step Three: Purge Yesterday's news pieces ------------------

news_piecesObjs = NewsPiece.objects.all()
num_deleted, _ = news_piecesObjs.delete()

print(f"Yesterday's TechJob Objects Deleted: {num_deleted}")

# ----------- Step Four: Add Today's news pieces ------------------

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
