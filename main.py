from fastapi import FastAPI, Path, Body, Query, Request, BackgroundTasks, Header, Depends
from typing import Union, Set, List
from modules.CRUD import SQL
from modules.EMAIL import EMAIL
from modules.SMS import SMS
from pydantic import BaseModel, Field, HttpUrl
import routers
import uvicorn
from middleware import MyMiddleware
app = FastAPI()
app.include_router(routers.router)
app.add_middleware(MyMiddleware, some_attribute="some_attribute_here_if_needed")

# 單元測試意外用
import sys, asyncio
if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#啟動mysql
@app.on_event("startup")
async def _startup():
    app.state.pool = await SQL.connect()


@app.get("/aioGetData", tags=['測試用'], summary='測試aiomysql')
async def aioGetData():
    """
        測試mysql 運作正常
    """
    return await SQL.get(app.state.pool, 'test')

@app.get('/')
def index():
    return {"msg":"Hello world"}


@app.get('/sendEmail', tags=['測試用'])
async def sendEmail(background_tasks: BackgroundTasks):
    # EMAIL.send()
    background_tasks.add_task(EMAIL.send)
    return '1|OK'


@app.get('/sendSMS', tags=['測試用'])
async def sendSMS(background_tasks: BackgroundTasks):
    # SMS.send()
    background_tasks.add_task(SMS.send)
    return '1|OK'

@app.get("/", tags=['學習用'])
async def user(*,
    user_id: int = Query(..., title="The ID of the user to get", gt=0)):
    return {'Hello': user_id}


# Header
@app.get("/getHeader/", tags=['學習用'])
async def getHeader(user_agent: Union[str, None] = Header(default=None)):
    return user_agent


# getSizeOfContent
@app.get('/content', tags=['學習用'])
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


@app.get('/getUser', tags=['學習用'])
async def getUser(new_user_id: str=Depends(user_reflect)):
    return new_user_id


# PATH
@app.get('/getID/{id}',  tags=['學習用'])
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


@app.post("/items/{item_id}", response_model=Item,  tags=['學習用'])
async def update_item(item_id: int, item: Item, user: User, importance: int = Body(gt=0)):
    results = {"item_id": item_id, "item": item, "user": user}
    return item




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
