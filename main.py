from fastapi import FastAPI
import pymysql
import asyncio
import aiomysql
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

db_settings = {
            "host": "192.46.224.179",
            "port": 3306,
            "user": "root",
            "password": "ikok1987",
            "db": 'shop',
            "charset": "utf8"
}
conn = pymysql.connect(**db_settings)

@app.get('/sqlSearch')
def sqlSearch():
    try:       # 建立連線
        conn.ping()
        with conn.cursor() as cursor:
                command = 'SELECT * FROM product;'
                cursor.execute(command)
                result = cursor.fetchall()
                cursor.close()
                
                return  result
    except Exception as ex:
      # 錯誤回報
        print(ex)

@app.on_event("startup")
async  def _startup():
    db_settings = {
        "host": "192.46.224.179",
        "port": 3306,
        "user": "root",
        "password": "ikok1987",
        "db": 'shop',
        "charset": "utf8",
    }
    app.state.pool = await aiomysql.create_pool(**db_settings)
    print('start done')
async def test_example(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM product;")
            return await cur.fetchall()



@app.get('/aioSqlSearch')
async def aioSqlSearch():
    return  await test_example(app.state.pool)
