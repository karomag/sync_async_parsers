import requests
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import User, Album, Photo, Todo, Post, Comment, Base

URL = 'https://jsonplaceholder.typicode.com'


def get_data(url: str = ''):
    try:
        r = requests.get(url)
        return r
    except Exception as ex:
        print(f'{ex}: Неизвестная ошибка загрузки.')


def create_users():
    users_lst = [User(
        id=user.get('id'),
        name=user.get('name'),
        username=user.get('username'),
        email=user.get('email'),
        address=user.get('address'),
        phone=user.get('phone'),
        website=user.get('website'),
        company=user.get('company')
    ) for user in get_data(URL + '/users').json()
    ]

    return users_lst


def create_todos():
    todos = [Todo(
        title=todo.get('title'),
        completed=todo.get('completed'),
        userId=todo.get('userId')
    ) for todo in get_data(URL + '/todos').json()
    ]
    return todos


def create_albums():
    albums = [Album(
        id=album.get('id'),
        title=album.get('title'),
        userId=album.get('userId')
    ) for album in get_data(URL + '/albums').json()
    ]
    return albums


def create_photos():
    photos = [Photo(
        title=photo.get('title'),
        url=photo.get('url'),
        thumbUrl=photo.get('thumbUrl'),
        albumId=photo.get('albumId')
    ) for photo in get_data(URL + '/photos').json()
    ]
    return photos


def create_posts():
    posts = [Post(
        id=post.get('id'),
        title=post.get('title'),
        userId=post.get('userId'),
    ) for post in get_data(URL + '/posts').json()
    ]
    return posts


def create_comments():
    comments = [Comment(
        name=comment.get('name'),
        email=comment.get('email'),
        body=comment.get('body'),
        postId=comment.get('postId')
    ) for comment in get_data(URL + '/comments').json()
    ]
    return comments


def main():
    engine = create_engine(
        "postgresql+psycopg2://karomag:password@localhost/sync_vs_async"
    )
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    session = Session()

    session.add_all(create_users())

    session.add_all(create_todos())
    session.add_all(create_albums())
    session.add_all(create_posts())

    session.add_all(create_photos())
    session.add_all(create_comments())

    session.commit()
    session.close()


if __name__ == '__main__':
    logger.info('Start the sync version!')
    main()
    logger.info('Finish the sync version!')
