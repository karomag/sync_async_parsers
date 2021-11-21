import requests
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import User, Album, Photo, Todo, Post, Comment, Base

URL = 'https://jsonplaceholder.typicode.com'


def get_data(url: str = '') -> requests.Response:
    r = requests.get(url)


def create_users(users):
    users_lst = [User(
        id=user.get('id'),
        name=user.get('name'),
        username=user.get('username'),
        email=user.get('email'),
        address=user.get('address'),
        phone=user.get('phone'),
        website=user.get('website'),
        company=user.get('company')
    ) for user in users
    ]
    return users_lst


def create_todos(todos):
    todos_lst = [Todo(
        title=todo.get('title'),
        completed=todo.get('completed'),
        userId=todo.get('userId')
    ) for todo in todos
    ]
    return todos_lst


def create_albums(albums):
    albums_lst = [Album(
        id=album.get('id'),
        title=album.get('title'),
        userId=album.get('userId')
    ) for album in albums
    ]
    return albums_lst


def create_photos(photos):
    photos_lst = [Photo(
        title=photo.get('title'),
        url=photo.get('url'),
        thumbUrl=photo.get('thumbUrl'),
        albumId=photo.get('albumId')
    ) for photo in photos
    ]
    return photos_lst


def create_posts(posts):
    posts_lst = [Post(
        id=post.get('id'),
        title=post.get('title'),
        userId=post.get('userId'),
    ) for post in posts
    ]
    return posts_lst


def create_comments(comments):
    comments_lst = [Comment(
        name=comment.get('name'),
        email=comment.get('email'),
        body=comment.get('body'),
        postId=comment.get('postId')
    ) for comment in comments
    ]
    return comments_lst


def main():
    engine = create_engine(
        "postgresql+psycopg2://karomag:password@localhost/sync_vs_async"
    )
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    session = Session()
    urls = {
        '/users': create_users,
        '/todos': create_todos,
        '/albums': create_albums,
        '/posts': create_posts,
        '/photos': create_photos,
        '/comments': create_comments,
    }
    for key, value in urls.items():
        raw_data = get_data(URL + key).json()
        session.add_all(value(raw_data))

    session.commit()
    session.close()


if __name__ == '__main__':
    logger.info('Start the sync version!')
    main()
    logger.info('Finish the sync version!')
