from user.routes import UserRouter


def setup_routes(app):
    UserRouter.setup(app)
