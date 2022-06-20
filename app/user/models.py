from datetime import datetime
from sqlalchemy import select, update
from app.db import UserTable


def updated_at(func):
    async def wrapped(*args, **kwargs):
        kwargs['updated_at'] = datetime.now()
        return await func(*args, **kwargs)

    return wrapped


class User:
    table = UserTable

    @classmethod
    async def serialize(cls, data, many=False):
        def get_item(_item):
            return {
                'id': _item.id,
                'username': _item.username,
                'created_at': _item.created_at.isoformat(),
                'updated_at': _item.updated_at.isoformat(),
            }

        if many:
            res = []
            for item in data:
                res.append(get_item(item))
            return res
        else:
            return get_item(data)

    @classmethod
    @updated_at
    async def create(cls, **kwargs):
        from app.main import database
        kwargs['created_at'] = datetime.now()

        async with database.session() as session:
            async with session.begin():
                instance = cls.table(**kwargs)
                session.add(instance)
            return await cls.serialize(instance)

    @classmethod
    @updated_at
    async def update(cls, instance, **kwargs):
        from app.main import database
        async with database.session() as session:
            async with session.begin():
                stmt = (update(cls.table)
                        .where(cls.table.id == instance.id)
                        .values(**kwargs)
                        .execution_options(synchronize_session="fetch"))
                await session.execute(stmt)

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

    @classmethod
    async def get_all(cls):
        from app.main import database

        async with database.session() as session:
            q = select(cls.table)
            resp = await session.execute(q)
        users = resp.scalars()
        data = await cls.serialize(users, many=True)
        return data

    @classmethod
    async def get_by_id(cls, _id):
        from app.main import database

        async with database.session() as session:
            stmt = select(cls.table).filter_by(id=_id)
            crt = await session.execute(stmt)
        return crt.scalars().first()
