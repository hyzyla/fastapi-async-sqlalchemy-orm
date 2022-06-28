from starlette.types import ASGIApp, Scope, Receive, Send

from app import session_scope, db


class SQLAlchemyMiddleware:
    """
    Middleware that do not create new session, but creates new session context.
    In new session context calling methods of `session` will create new session
    automatically
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        with session_scope.set_scoped_context():
            try:
                await self.app(scope, receive, send)
            finally:
                # free memory after every request
                await db.session.remove()
