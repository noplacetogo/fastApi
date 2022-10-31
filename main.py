from fastapi import FastAPI
import mysql as sql

app = FastAPI()



@app.on_event("startup")
async  def _startup():
   app.state.pool  = await sql.SQL.connect()

@app.get("/aioGetData")
async  def aioGetData():
   return await sql.SQL.get(app.state.pool,'product')


@app.get("/getData")
def getData():
   return sql.DB.get()
