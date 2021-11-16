from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import JSONB


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    address = Column(JSONB)
    phone = Column(String(30))
    website = Column(String(100))
    company = Column(JSONB)
    todos = relationship("Todo", back_populates="user")
    albums = relationship("Album", back_populates="user")
    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return f'{self.__class__.__name__} {self.username}'


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    completed = Column(Boolean)
    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="todos")

    def __repr__(self):
        return f'{self.__class__.__name__} id: {self.id} TODO: {self.title} ' \
               f'completed: {self.completed} (User id: {self.userId})'


class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="albums")
    photos = relationship("Photo", back_populates="album")

    def __repr__(self):
        return f'{self.__class__.__name__} id: {self.id} Title: {self.title} ' \
               f'(User id: {self.userId})'


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    url = Column(String(250))
    thumbUrl = Column(String(250))
    albumId = Column(Integer, ForeignKey('albums.id'))
    album = relationship("Album", back_populates="photos")

    def __repr__(self):
        return f'{self.__class__.__name__} id: {self.id} Title: {self.title}' \
               f'Album id: {self.userId}'


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    body = Column(Text)
    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="posts")

    def __repr__(self):
        return f'{self.__class__.__name__} id: {self.id} Title: {self.title} ' \
               f'(User id: {self.userId})'


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    body = Column(Text)
    postId = Column(Integer, ForeignKey('posts.id'))
    posts = relationship("Post", back_populates="comments")

    def __repr__(self):
        return f'{self.__class__.__name__} id: {self.id} Title: {self.title} ' \
               f'(Post id: {self.postId})'
