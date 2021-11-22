import asyncio
import aiohttp
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from db.models import User, Album, Photo, Todo, Post, Comment, Base

URL = 'https://jsonplaceholder.typicode.com'


async def get_data(url: str, session: aiohttp.ClientSession):
    logger.info('Start {}!', url)
    async with session.get(url, allow_redirects=True) as response:
        data = await response.json()
        logger.info('Finish {}!', url)
        return data


async def create_users(session):
    logger.info('Start!')
    async with aiohttp.ClientSession() as httpsession:
        users = await get_data(URL + '/users', httpsession)
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
    session.add_all(users_lst)
    logger.info('Finish!')


async def create_todos(session):
    logger.info('Start!')
    async with aiohttp.ClientSession() as httpsession:
        todos = await get_data(URL + '/todos', httpsession)
    todos_lst = [Todo(
        title=todo.get('title'),
        completed=todo.get('completed'),
        userId=todo.get('userId')
    ) for todo in todos
    ]
    session.add_all(todos_lst)
    logger.info('Finish!')


async def create_albums(session):
    logger.info('Start!')
    async with aiohttp.ClientSession() as httpsession:
        albums = await get_data(URL + '/albums', httpsession)
    albums_lst = [Album(
        id=album.get('id'),
        title=album.get('title'),
        userId=album.get('userId')
    ) for album in albums
    ]
    session.add_all(albums_lst)
    logger.info('Finish!')


async def create_photos(session):
    logger.info('Start!')
    async with aiohttp.ClientSession() as httpsession:
        photos = await get_data(URL + '/photos', httpsession)
    photos_lst = [Photo(
        title=photo.get('title'),
        url=photo.get('url'),
        thumbUrl=photo.get('thumbUrl'),
        albumId=photo.get('albumId')
    ) for photo in photos
    ]
    session.add_all(photos_lst)
    logger.info('Finish!')


async def create_posts(session):
    logger.info('Start!')
    async with aiohttp.ClientSession() as httpsession:
        posts = await get_data(URL + '/posts', httpsession)
    posts_lst = [Post(
        id=post.get('id'),
        title=post.get('title'),
        userId=post.get('userId'),
    ) for post in posts
    ]
    session.add_all(posts_lst)
    logger.info('Finish!')


async def create_comments(session):
    logger.info('Start!')
    async with aiohttp.ClientSession() as httpsession:
        comments = await get_data(URL + '/comments', httpsession)
    comments_lst = [Comment(
        name=comment.get('name'),
        email=comment.get('email'),
        body=comment.get('body'),
        postId=comment.get('postId')
    ) for comment in comments
    ]
    session.add_all(comments_lst)
    logger.info('Finish!')


async def async_main():
    engine = create_async_engine(
        "postgresql+asyncpg://karomag:password@localhost/sync_vs_async"
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    coros = [
        create_users,
        create_todos,
        create_albums,
        create_posts,
        create_photos,
        create_comments,
    ]

    async with async_session() as session:
        async with session.begin():
            tasks = []
            for func in coros:
                task = asyncio.create_task(func(session))
                tasks.append(task)
            logger.info('Start gather!')
            await asyncio.gather(*tasks)
            logger.info('Finish gather!')
        logger.info('Session close')

    await engine.dispose()


if __name__ == '__main__':
    logger.info('Start the async version!')
    asyncio.run(async_main())
    logger.info('Finish the async version!')
