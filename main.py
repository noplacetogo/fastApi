from fastapi import FastAPI
from modules.CRUD import SQL

app = FastAPI()



@app.on_event("startup")
async  def _startup():
   app.state.pool  = await SQL.connect()

@app.get("/aioGetData")
async  def aioGetData():
   return await SQL.get(app.state.pool,'test')



