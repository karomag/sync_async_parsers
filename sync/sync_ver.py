import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
from sqlalchemy import create_engine
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


def main():
    engine = create_engine("postgresql+psycopg2://karomag:password@localhost/sync_vs_async")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    users = [User(
            name=user.get('name'),
            username=user.get('username'),
            email=user.get('email'),
            address=user.get('address'),
            phone=user.get('phone'),
            website=user.get('website'),
            company=user.get('company')
            ) for user in get_users()
    ]
    with Session.begin() as session:
        session.add_all(users)
        # session.commit()

    for user in users:
        todos = [Todo(
            title=todo.get('title'),
            completed=todo.get('completed'),
            userId=user.id
            ) for todo in get_todos(user)
        ]
        with Session.begin() as session:
            session.add_all(todos)


if __name__ == '__main__':
    main()
