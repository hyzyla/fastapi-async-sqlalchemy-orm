# FastAPI + async SQLAlchemy ORM + async_scoped_session example

## Features:
* Async FastAPI
* Async SQLAlchemy ORM
* async_scoped_session (you can access session by global variable)


## Run
```shell
poetry install
poetry run uvicorn app.main:app
```


# How to start session

Session will be started automatically on a first request to database: commit, query, delete, etc
```python
from fastapi import FastAPI
from app import db, models

app = FastAPI()

@app.post("/todo")
async def create_todo():

    todo = models.Todo()
    db.session.add(todo)

     # new session will be created automatically here
    await db.session.commit()
```


# How it works
```
Web Server          Web Framework        SQLAlchemy ORM Code
--------------      --------------       ------------------------------
startup        ->   Web framework        # Session registry is established
                    initializes          # file: app/db.py
                                         AsyncSessionFactory = sessionmaker(
                                             bind=engine,
                                             class_=AsyncSession,
                                         )
                                         session = async_scoped_session(
                                             session_factory=AsyncSessionFactory,
                                             scopefunc=session_scope.get_session_context,
                                         )

incoming
web request    ->   web request     ->   # SQLAlchemyMiddleware create new scoped context.
                                         # That do nothing with ORM and the database itself,
                                         # it's just a marker for SQLAlchemy to create a new
                                         # instance of AsyncSession if some make some query
                                         # using `session` created during startup.
                                         # file: app/middlewares.py
                                         with session_scope.set_scoped_context():
                                             ...

                                         # the Session registry can otherwise
                                         # be used at any time, creating the
                                         # request-local AsyncSession() if not present,
                                         # or returning the existing one
                                         # file: app/main.py
                                         await db.session.query(MyClass) # ...

                                         await db.session..add(some_object) # ...

                                         # if data was modified, commit the
                                         # transaction
                                         await db.session.commit()

                    web request ends  -> # SQLAlchemyMiddleware at the end of the request
                                         # removes a session from the registry. Also
                                         # context manager `with session_scope.set_scoped_context()`
                                         # removes the indicator created at the beginning of
                                         # the request.
                                         # file: app/middlewares.py
                                         db.session.remove()

                    sends output      <-
outgoing web    <-
response
```
