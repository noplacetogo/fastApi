from fastapi import APIRouter, Request

from modules.CRUD import SQL
from modules.TOOLS import parse_params_to_sql

router = APIRouter()


@router.get("/{table}", tags=["API"])
async def getData(request: Request, table: str) -> tuple:
    if not await request.query_params:
        return await SQL.get(request.app.state.pool, table)
    else:
        res = await SQL.query(request.app.state.pool,
                              table, f"SELECT * FROM {table} WHERE {parse_params_to_sql(await request.query_params)}")
        return res


@router.post("/{table}", tags=["API"])
async def postData(request: Request, table: str):
    """
        POST 可接收JSON, FORM資料
    """
    payload = dict(await request.form())
    try:
        payload.update(await request.json())
    except Exception as e:
        pass
    await SQL.update(request.app.state.pool, table, payload)
    return "1|OK"
