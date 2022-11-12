from fastapi import FastAPI, Path, Body, Query, Request, BackgroundTasks, Header, Depends
from typing import Union, Set, List
from modules.CRUD import SQL
from pydantic import BaseModel, Field, HttpUrl
import routers
import uvicorn
from middleware import MyMiddleware
app = FastAPI()
app.include_router(routers.router)
app.add_middleware(MyMiddleware, some_attribute="some_attribute_here_if_needed")

#啟動mysql
@app.on_event("startup")
async def _startup():
    app.state.pool = await SQL.connect()


@app.get("/aioGetData", tags=['正常'], summary='測試aiomysql')
async def aioGetData():
    """
        測試mysql 運作正常
    """
    return await SQL.get(app.state.pool, 'test')


@app.get("/", tags=['測試'])
async def user(*,
    user_id: int = Query(..., title="The ID of the user to get", gt=0)):
    return {'Hello': user_id}


# Header
@app.get("/getHeader/", tags=['測試'])
async def getHeader(user_agent: Union[str, None] = Header(default=None)):
    return user_agent


# getSizeOfContent
@app.get('/content')
async def getContent(request: Request):
    return request.headers
# Depend
# Query 較驗
# Field、Query、Body、PATH
# title
# describe
# min_length, max_length, 正則表達式
# gt, ge, lt, le
async def user_reflect(user_id: Union[str, None] = Query(default=None, max_length=50)):
    return user_id


@app.get('/getUser', tags=['測試'])
async def getUser(new_user_id: str=Depends(user_reflect)):
    return new_user_id


# PATH
@app.get('/getID/{id}')
async def getID(*, id: int= Path(title='ING', gt=0)):
    return id


# BaseModel
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: Union[float, None] = Field(default=0, title='The Price', gt=0)
    tax: Union[float, None] = None
    message: List[str] = []
    imageUrl: HttpUrl


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.post("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item, user: User, importance: int = Body(gt=0)):
    results = {"item_id": item_id, "item": item, "user": user}
    return item


# 示範BackgroudTask
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
