import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

#models
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    score = Column(Integer)
    comment_count = Column(Integer)
    timestamp = Column(DateTime)
    image = Column(String)
    video_url = Column(String)


def connect_to_database(db_config):
    db_host = db_config['host']
    db_port = db_config['port']
    db_name = db_config['name']
    db_user = db_config['user']
    db_password = db_config['password']

    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    return engine


def save_posts_to_database(posts, db_config):
    engine = connect_to_database(db_config)
    Session = sessionmaker(bind=engine)
    session = Session()

    existing_ids = session.query(Post.id).all()
    existing_ids = set(row[0] for row in existing_ids)

    new_posts = []
    for post in posts:
        if post.id not in existing_ids:
            new_posts.append(post)

    session.add_all(new_posts)
    session.commit()
    session.close()
