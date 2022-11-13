from fastapi import APIRouter, Request
from modules.CRUD import SQL
from modules.TOOLS import parse_params_to_sql
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/{table}", tags=["API"])
async def getData(request: Request, table: str) -> tuple:
    if not request.query_params:
        json_compatible_item_data = jsonable_encoder(await SQL.get(request.app.state.pool, table))
        return JSONResponse(content=json_compatible_item_data)

    else:
        res = await SQL.query(request.app.state.pool,
                              table, f"SELECT * FROM {table} WHERE {parse_params_to_sql(request.query_params)}")
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)


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
