from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Optional
import feedparser
from bs4 import BeautifulSoup
import requests

router = APIRouter()


class Article(BaseModel):
    title: str
    link: str
    pubDate: str
    imageUrl: Optional[str] = None


@router.get("/habr/articles", response_model=List[Article])
async def get_habr_articles():
    url = "https://habr.com/ru/rss/all/all/?fl=ru"
    feed = feedparser.parse(requests.get(url).content)

    articles: List[Article] = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        pub_date = entry.published

        # Парсим description как HTML
        soup = BeautifulSoup(entry.description, "html.parser")
        img = soup.find("img")
        image_url = img["src"] if img else None

        articles.append(Article(title=title, link=link, pubDate=pub_date, imageUrl=image_url))

    return articles
