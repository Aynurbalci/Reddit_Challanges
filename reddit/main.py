import json
from databaseProceses.database import write_to_db

def read_posts_from_json(filename: str):
    with open(filename) as file:
        posts = json.load(file)
        print(posts)
        return posts


def main():
    filename = "reddit/posts.json"
    posts = read_posts_from_json(filename)
    for post in posts:
        write_to_db(post)



if __name__ == "__main__":
    main()
