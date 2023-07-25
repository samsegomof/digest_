from typing import List

from fastapi import HTTPException

from source.config import Settings
from source.database import async_session_maker
from source.api.schemas import SubscriptionSchema, PostSchema
from source.api.models import User, Subscription, Post, Digest
from source.base_service import BaseService


class UserService(BaseService):
    model = User

    @classmethod
    async def get_user_or_404(cls, user_id: int):
        user = await cls.get_object_or_none(id=user_id)

        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        return user

    @classmethod
    async def get_user_subscriptions(cls, user: User) -> List[SubscriptionSchema]:
        subscriptions = await SubscriptionService.get_subscriptions_by_user(user)
        return subscriptions


class PostService(BaseService):
    model = Post

    @classmethod
    async def get_posts_by_subscription(cls, subscription: Subscription) -> List[PostSchema]:
        return await subscription.posts

    @classmethod
    async def filter_posts(cls, posts: List[PostSchema]) -> List[PostSchema]:

        filtered_posts = [post for post in posts if cls._is_post_popular(post)]

        return filtered_posts

    @staticmethod
    def _is_post_popular(post: PostSchema) -> bool:
        return post.popularity >= Settings.min_popularity


class SubscriptionService(BaseService):
    model = Subscription

    @classmethod
    async def get_subscriptions_by_user(cls, user: User) -> List[SubscriptionSchema]:
        async with async_session_maker() as session:
            # query = session.execute(cls.model.__table__.select().where(cls.model.user_subscriptions == user))
            # subscriptions = await query.fetchall()
            # return subscriptions
            query = session.query(cls.model).filter(cls.model.user_subscriptions.has(id=user.id))
            subscriptions = await query.all()
            return subscriptions

    @staticmethod
    async def get_subscription_by_id(sub_id: int) -> Subscription:
        async with async_session_maker() as session:
            # query = session.execute(Subscription.__table__.select().where(Subscription.id == sub_id))
            # subscription = await query.fetchone()
            # return subscription
            query = session.query(Subscription).filter(Subscription.id == sub_id)
            subscription = await query.first()
            return subscription


class DigestService(BaseService):
    model = Digest

    @classmethod
    async def generate_digest(cls, user_id: int) -> Digest:
        user = await UserService.get_user_or_404(user_id=user_id)

        subscriptions = await UserService.get_user_subscriptions(user)

        collected_posts = []

        for subscription in subscriptions:
            subscription_obj = await SubscriptionService.get_subscriptions_by_id(subscription.id)
            posts = await PostService.get_posts_by_subscription(subscription_obj)
            collected_posts.extend(posts)

        filtered_posts = await PostService.filter_posts(collected_posts)

        digest = await super().create(user=user, posts=filtered_posts)

        return digest
