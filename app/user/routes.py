import json

from aiohttp import web

from app.user.models import User


class UserHandler:
    @staticmethod
    async def get_users(request):
        users = await User.get_all()
        return web.Response(body=json.dumps(users), content_type='application/json')

    @staticmethod
    async def get_user_by_id(request):
        _id = request.match_info.get('id')
        user = await User.get_by_id(_id)
        data = await User.serialize(user)
        return web.Response(body=json.dumps(data), content_type='application/json')

    @staticmethod
    async def create_user(request):
        data = await request.json()
        # TODO add validator
        user = await User.create(**data)
        return web.Response(body=json.dumps(user), status=201, content_type='application/json')

    @staticmethod
    async def update_user(request):
        _id = request.match_info.get('id')
        data = await request.json()
        # TODO add validator
        user = await User.get_by_id(_id)
        await User.update(user, **data)
        data = await User.serialize(user)
        return web.Response(body=json.dumps(data), status=200, content_type='application/json')


class UserRouter:

    @staticmethod
    def setup(app):
        app.router.add_get('/users/', UserHandler.get_users, name='users')
        app.router.add_get('/users/{id}/', UserHandler.get_user_by_id, name='user')
        app.router.add_post('/users/', UserHandler.create_user, name='create-user')
        app.router.add_patch('/users/{id}/', UserHandler.update_user, name='update-user')

