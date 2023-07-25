import json

from source.database import async_session_maker
from source.api.models import User, Subscription, Post, Digest


class DataLoader:
    def __init__(self, json_file: str):
        self.json_file = json_file

    async def load_fixtures(self):
        with open(self.json_file, 'r') as f:
            data = json.load(f)

        async with async_session_maker() as session:
            await self.add_users(session, data['users'])
            await self.add_subscriptions(session, data['subscriptions'])
            await self.add_posts(session, data['posts'])
            await self.add_digests(session, data['digests'])

    @staticmethod
    async def add_users(session, users_data):
        for user_data in users_data:
            user = User(**user_data)
            session.add(user)
        await session.commit()

    @staticmethod
    async def add_subscriptions(session, subscriptions_data):
        for subscription_data in subscriptions_data:
            subscription = Subscription(**subscription_data)
            session.add(subscription)
        await session.commit()

    @staticmethod
    async def add_posts(session, posts_data):
        for post_data in posts_data:
            post = Post(**post_data)
            session.add(post)
        await session.commit()

    @staticmethod
    async def add_digests(session, digests_data):
        for digest_data in digests_data:
            digest = Digest(**digest_data)
            session.add(digest)
        await session.commit()


if __name__ == "__main__":
    import asyncio

    loader = DataLoader('fixtures.json')
    asyncio.run(loader.load_fixtures())
    print('The data from the file has been added to the database!')
