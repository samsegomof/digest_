from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from source.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)

    subscriptions = relationship(
        'Subscription',
        backref='user',
        cascade='all, delete'
    )


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    source = Column(String(150))
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    posts = relationship(
        'Post',
        backref='subscription',
        cascade='all, delete',
        lazy='dynamic'
    )
    user_subscriptions = relationship('User', back_populates='subscriptions')


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    popularity = Column(Integer, nullable=False, default=0)
    subscription_id = Column(
        Integer,
        ForeignKey('subscriptions.id', ondelete='CASCADE')
    )
    post_subscription = relationship('Subscription', back_populates='posts')


class Digest(Base):
    __tablename__ = 'digests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    posts = Column(ARRAY(item_type=String))
