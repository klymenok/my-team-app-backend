from aiohttp import web

from db import Database
from router import setup_routes

DB_NAME = 'teamapp'  # TODO: move to .env

app = web.Application()

setup_routes(app)

database = Database(DB_NAME)

if __name__ == '__main__':
    web.run_app(app)
