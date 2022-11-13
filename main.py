import uvicorn
from fastapi import FastAPI
from modules.CRUD import SQL

app = FastAPI()



@app.on_event("startup")
async  def _startup():
   app.state.pool  = await SQL.connect()

@app.get("/aioGetData/{table}")
async  def aioGetData(table: str):
   return await SQL.get(app.state.pool, table)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
