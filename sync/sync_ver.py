import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from db.models import User, Album, Photo, Todo, Post, Comment, Base

URL = 'https://jsonplaceholder.typicode.com'


def get_users():
    try:
        r = requests.get(URL + '/users')
        return r.json()
    except ConnectionError:
        print('Ошибка соединения.')
    except HTTPError:
        print('Ошибка запроса.')
    except Timeout:
        print('Время ожидания ответа истекло.')
    except Exception as ex:
        print(f'{ex}: Неизвестная ошибка загрузки.')


def create_users(session):
    users_lst = [User(
        id=user.get('id'),
        name=user.get('name'),
        username=user.get('username'),
        email=user.get('email'),
        address=user.get('address'),
        phone=user.get('phone'),
        website=user.get('website'),
        company=user.get('company')
    ) for user in get_users()
    ]

    try:
        session.add_all(users_lst)
        session.commit()
    except IntegrityError as ex:
        print(ex)
    # finally:
    #     session.close()


def get_todos(user: User):
    try:
        r = requests.get(URL + '/users/' + str(user.id) + '/todos')
        return r.json()
    except ConnectionError:
        print('Ошибка соединения.')
    except HTTPError:
        print('Ошибка запроса.')
    except Timeout:
        print('Время ожидания ответа истекло.')
    except Exception as ex:
        print(f'{ex}: Неизвестная ошибка загрузки.')


def create_todos(session):
    users = session.query(User).all()
    for user in users:
        todos = [Todo(
            title=todo.get('title'),
            completed=todo.get('completed'),
            userId=user.id
        ) for todo in get_todos(user)
        ]
        try:
            session.add_all(todos)
            session.commit()
        except IntegrityError as ex:
            print(ex)
        # finally:
        #     session.close()


def get_albums(user: User):
    try:
        r = requests.get(URL + '/users/' + str(user.id) + '/albums')
        return r.json()
    except ConnectionError:
        print('Ошибка соединения.')
    except HTTPError:
        print('Ошибка запроса.')
    except Timeout:
        print('Время ожидания ответа истекло.')
    except Exception as ex:
        print(f'{ex}: Неизвестная ошибка загрузки.')


def create_albums(session):
    users = session.query(User).all()
    for user in users:
        albums = [Album(
            id=album.get('id'),
            title=album.get('title'),
            userId=user.id
        ) for album in get_albums(user)
        ]
        try:
            session.add_all(albums)
            session.commit()
        except IntegrityError as ex:
            print(ex)
        # finally:
        #     session.close()


def get_photos(album: Album):
    try:
        r = requests.get(URL + '/albums/' + str(album.id) + '/photos')
        return r.json()
    except ConnectionError:
        print('Ошибка соединения.')
    except HTTPError:
        print('Ошибка запроса.')
    except Timeout:
        print('Время ожидания ответа истекло.')
    except Exception as ex:
        print(f'{ex}: Неизвестная ошибка загрузки.')


def create_photos(session):
    albums = session.query(Album).all()
    for album in albums:
        photos = [Photo(
            title=photo.get('title'),
            url=photo.get('url'),
            thumbUrl=photo.get('thumbUrl'),
            albumId=album.id
        ) for photo in get_photos(album)
        ]
        try:
            session.add_all(photos)
            session.commit()
        except IntegrityError as ex:
            print(ex)
        # finally:
        #     session.close()


def get_posts(user: User):
    try:
        r = requests.get(URL + '/users/' + str(user.id) + '/posts')
        return r.json()
    except ConnectionError:
        print('Ошибка соединения.')
    except HTTPError:
        print('Ошибка запроса.')
    except Timeout:
        print('Время ожидания ответа истекло.')
    except Exception as ex:
        print(f'{ex}: Неизвестная ошибка загрузки.')


def create_posts(session):
    users = session.query(User).all()
    for user in users:
        posts = [Post(
            id=post.get('id'),
            title=post.get('title'),
            userId=user.id
        ) for post in get_posts(user)
        ]
        try:
            session.add_all(posts)
            session.commit()
        except IntegrityError as ex:
            print(ex)
        # finally:
        #     session.close()


def get_comments(post: Post):
    try:
        r = requests.get(URL + '/posts/' + str(post.id) + '/comments')
        return r.json()
    except ConnectionError:
        print('Ошибка соединения.')
    except HTTPError:
        print('Ошибка запроса.')
    except Timeout:
        print('Время ожидания ответа истекло.')
    except Exception as ex:
        print(f'{ex}: Неизвестная ошибка загрузки.')


def create_comments(session):
    posts = session.query(Post).all()
    for post in posts:
        comments = [Comment(
            name=comment.get('name'),
            email=comment.get('email'),
            body=comment.get('body'),
            postId=post.id
        ) for comment in get_comments(post)
        ]
        try:
            session.add_all(comments)
            session.commit()
        except IntegrityError as ex:
            print(ex)
        # finally:
        #     session.close()


def main():
    engine = create_engine("postgresql+psycopg2://karomag:password@localhost/sync_vs_async")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    session = Session()
    create_users(session)
    session.close()

    session = Session()
    create_todos(session)
    session.close()

    session = Session()
    create_albums(session)
    session.close()
    session = Session()
    create_photos(session)
    session.close()

    session = Session()
    create_posts(session)
    session.close()
    session = Session()
    create_comments(session)
    session.close()


if __name__ == '__main__':
    main()
