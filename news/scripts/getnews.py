import feedparser
import requests
from bs4 import BeautifulSoup

news = []

# ----------- Step One: Get News & Articles from RSS Feeds ------------------

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

sources = [
    # ---- Media Keyword: media_content
    "https://www.engadget.com/rss.xml", 
    "https://www.cnet.com/rss/news/",
    "https://www.freecodecamp.org/news/rss/",

    # ---- Media Keyword: media_thumbnail
    "https://www.wired.com/feed/tag/ai/latest/rss",
    "https://www.wired.com/feed/category/ideas/latest/rss",
    "https://feeds.dzone.com/home",

    # # ---- No Media Keyword
    "https://techpoint.africa/feed/",
    "https://disrupt-africa.com/feed/",
    "https://www.itnewsafrica.com/feed/",
    "https://techcabal.com/feed/",
    "https://techcityng.com/feed/",
    "https://www.appsafrica.com/feed/"
]

# function to source images for rss feed entries with no media-content
def getImageUrl(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    images = soup.find_all("img")
    count = 0

    for image in images:
        if image.has_attr("src"):
            count += 1
            if count == round(len(images) / 6):
                return(image["src"])

    for img in images:
        print(img)     
    print(len(images))

# Fetch news from sources
for source in sources:
    feed = feedparser.parse(source)
    for entry in feed.entries:
        news_item = {
            "source": feed.feed.title,
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
