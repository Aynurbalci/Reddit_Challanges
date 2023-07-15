from flask import Flask, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Reddit.DatabaseProceses.Database import connect_to_database, Post
from configparser import ConfigParser

app = Flask(__name__)

@app.route('/posts', methods=['GET'])
def get_posts():
    config = ConfigParser()
    config.read('config.ini')

    reddit_config = {
        'subreddit': config.get('Reddit', 'subreddit'),
        'search_keyword': config.get('Reddit', 'search_keyword'),
        'username': config.get('Reddit', 'username'),
        'password': config.get('Reddit', 'password')
    }

    db_config = {
        'host': config.get('Database', 'host'),
        'port': config.get('Database', 'port'),
        'name': config.get('Database', 'name'),
        'user': config.get('Database', 'user'),
        'password': config.get('Database', 'password')
    }

    engine = connect_to_database(db_config)
    Session = sessionmaker(bind=engine)
    session = Session()

    posts = session.query(Post).all()
    post_list = []

    for post in posts:
        post_dict = {
            'id': post.id,
            'title': post.title,
            'author': post.author,
            'score': post.score,
            'comment_count': post.comment_count,
            'timestamp': post.timestamp.isoformat(),
            'image': post.image,
            'video_url': post.video_url
        }
        post_list.append(post_dict)

    session.close()

    return jsonify(post_list)

if __name__ == '__main__':
    app.run()
