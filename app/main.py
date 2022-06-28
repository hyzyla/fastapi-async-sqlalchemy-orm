import uuid

from fastapi import FastAPI

from app import db, middlewares, session_scope

app = FastAPI(
    on_startup=[db.create_all_tables],
)
app.add_middleware(middlewares.SQLAlchemyMiddleware)


@app.post("/test")
async def write():
    request_id = str(uuid.uuid4())
    session_id = session_scope.get_session_context()

    event = db.Event(
        session_id=session_id,
        request_id=request_id,
    )
    db.session.add(event)
    await db.session.commit()

