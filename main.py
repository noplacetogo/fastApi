from fastapi import FastAPI, Path, Body, Query, Request, BackgroundTasks, Header, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from typing import Union, Set, List
from modules.CRUD import SQL
from pydantic import BaseModel, Field, HttpUrl
import routers
import uvicorn
from middleware import MyMiddleware
# slow
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
# Router
app.include_router(routers.router)
# Middle
app.add_middleware(MyMiddleware, some_attribute="some_attribute_here_if_needed")
# limit api
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# login token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="member/token")
# cors
origins = [
    'https://cdpn.io'
    # "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#啟動mysql
@app.on_event("startup")
async def _startup():
    app.state.pool = await SQL.connect()


@app.get("/aioGetData", tags=['測試用'], summary='測試aiomysql')
@limiter.limit("5/minute")
async def aioGetData(request: Request):
    """
        測試mysql 運作正常
    """
    return await SQL.get(app.state.pool, 'product')


@app.get('/')
def index():
    return {"msg": "Hello world"}

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
    uvicorn.run(app, host="0.0.0.0", port=8000)

