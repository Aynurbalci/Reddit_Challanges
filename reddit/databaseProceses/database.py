from sqlalchemy.orm import sessionmaker
from datetime import datetime

from sqlalchemy import create_engine
from reddit.models.database_models import Post
from reddit.env import db_host, db_port, db_name, db_user, db_password

# Veritabanı bağlantısı
engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def write_to_db(post):
    db = SessionLocal()
    try:
        db_post = Post(
            id=post['id'],
            title=post['title'],
            author=post['author'],
            score=int(post['score']),
            comment_count=int(post['comment_count']),
            timestamp=datetime.strptime(post['timestamp'], "%Y-%m-%d %H:%M:%S"),
            url=post['url'],
            content=post['content']
        )
        db.add(db_post)
        db.commit()
        print("Veri başarıyla veritabanına eklendi!")
    except Exception as e:
        db.rollback()
        print(f"Veritabanına yazarken hata oluştu: {str(e)}")
    finally:
        db.close()
