from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from Reddit.Api.RedditElements import convert_to_datetime
from Reddit.DatabaseProceses.Database import save_posts_to_database

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    score = Column(Integer)
    comment_count = Column(Integer)
    timestamp = Column(DateTime)
    image = Column(String)
    video_url = Column(String)

def extract_comment_count(text):
    try:
        count = int(text)
        return count
    except ValueError:
        if text.endswith("comment"):
            return 1
        elif text.endswith("comments"):
            return int(text.split()[0])
        else:
            return None

def login_to_reddit(page, username, password):
    page.goto("https://www.reddit.com/login/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_load_state()

def scrape_reddit(reddit_config, db_config):
    subreddit = reddit_config['subreddit']
    search_keyword = reddit_config['search_keyword']
    username = reddit_config['username']
    password = reddit_config['password']

    posts = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        login_to_reddit(page, username, password)

        page.goto(f"https://www.reddit.com/r/{subreddit}/new/", timeout=12000000)

        page.fill('input[name="q"]', search_keyword)
        page.press('input[name="q"]', 'Enter')

        page.wait_for_load_state()

        content = page.content()

        soup = BeautifulSoup(content, "html.parser")

        post_containers = soup.select("div._1oQyIsiPHYt6nx7VOmd1sz")
#css selector xpath?
        for container in post_containers:
            title_element = container.select_one("h3._eYtD2XCVieq6emjKBH3m")
            author_element = container.select_one("a._2tbHP6ZydRpjI44J3syuqC")
            score_element = container.select_one("div._1rZYMD_4xY3gRcSS3p8ODO")
            comment_count_element = container.select_one("span.FHCV02u6Cp2zYL0fhQPsO")
            timestamp_element = container.select_one("span._2VF2J19pUIMSLJFky-7PEI")
            image_element = container.select_one("img._2_tDEnGMLxpM6uOa2kaDB3")
            video_element = container.select_one("video._2S_jMRr63r3lFfXed_TTgC source")

            if title_element and author_element and score_element and comment_count_element and timestamp_element:
                title = title_element.text.strip()
                author = author_element.text.strip()
                score_text = score_element.text.strip()
                comment_count_text = comment_count_element.text.strip()
                timestamp = timestamp_element.text.strip()
                datetime_obj = convert_to_datetime(timestamp)

                if image_element:
                    image = image_element["src"]
                else:
                    image = None

                if video_element:
                    video_url = video_element["src"]
                else:
                    video_url = None

                try:
                    score = int(score_text)
                except ValueError:
                    score = None

                comment_count = extract_comment_count(comment_count_text)
#eksik içerik ?
                if image or video_url:
                    post = Post(
                        title=title,
                        author=author,
                        score=score,
                        comment_count=comment_count,
                        timestamp=datetime_obj,
                        image=image,
                        video_url=video_url
                    )

                    posts.append(post)

        browser.close()

        save_posts_to_database(posts, db_config)