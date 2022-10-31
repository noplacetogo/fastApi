from fastapi import FastAPI
import mysql as sql

app = FastAPI()



@app.on_event("startup")
async  def _startup():
   app.state.pool  = await sql.SQL.connect()

@app.get("/getData")
async  def getData():
   return await sql.SQL.(app.state.pool,'product')
