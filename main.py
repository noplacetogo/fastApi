from fastapi import FastAPI
import pymysql
import asyncio
import aiomysql
import mysql as sql
app = FastAPI()



@app.on_event("startup")
async  def _startup():
   app.state.pool  = await sql.SQL()

