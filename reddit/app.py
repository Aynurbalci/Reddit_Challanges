import json
from httpx import AsyncClient
from datetime import datetime
import os
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
app = FastAPI()

class Post(BaseModel):
    id: str
    title: str
    author: str
    score: int
    comment_count: int
    timestamp: str
    url: str
    content: str
#dosya yapısı poetry - dosyaların yeri ? poetry kullan ? docker compose ? database - docker , dosyalarda yığılma (api ?)
#diğer kaynaklardan veri ?
async def fetch_posts(subreddit: str):
    async with AsyncClient() as client:
        url = f"https://www.reddit.com/r/{subreddit}/new.json"
        headers = {"Aynur": "Test"}

        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            posts = data["data"]["children"]

            post_list = []
            for post in posts:
                post_data = post["data"]
                timestamp = datetime.fromtimestamp(post_data['created_utc']).strftime("%Y-%m-%d %H:%M:%S")

                item = Post(
                    id=post_data.get('id'),
                    title=post_data.get('title'),
                    author=post_data.get('author'),
                    score=post_data.get('score'),
                    comment_count=post_data.get('num_comments'),
                    timestamp=timestamp,
                    url=post_data.get('url'),
                    content=post_data.get('selftext', '')
                )

                post_list.append(item.model_dump())

            return post_list
        else:
            raise Exception("postlar alınamadı")

def write_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def create_json_file(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)

async def update_posts(background_tasks: BackgroundTasks, subreddits: list):
    try:
        all_posts = []
        for subreddit in subreddits:
            posts = await fetch_posts(subreddit)
            all_posts.extend(posts)

        current_posts = []

        if os.path.exists('posts.json'):
            with open('posts.json') as file:
                current_posts = json.load(file)

        new_posts = [post for post in all_posts if post not in current_posts]
        combined_posts = current_posts + new_posts

        write_to_json(combined_posts, 'posts.json')

        if new_posts:
            print("Yeni veriler")
            for post in new_posts:
                print(post)
            print()
    except Exception as e:
        print(f"Error: {str(e)}")

    # 10 dakika sonra tekrar veri çeker
    background_tasks.add_task(update_posts, background_tasks, subreddits)

@app.get("/posts/{subreddit}")
async def get_posts(subreddit: str):
    try:
        with open('posts.json') as file:
            posts = json.load(file)
            return posts
    except Exception as e:
        return {"error": str(e)}

@app.on_event("startup")
async def startup_event():
    create_json_file('posts.json')
    background_tasks = BackgroundTasks()
    subreddits = ["Phishing Crashers", "Xeroxeddolly", "m-p-3"]
    background_tasks.add_task(update_posts, background_tasks, subreddits)

@app.on_event("shutdown")
async def shutdown_event():
    pass

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)