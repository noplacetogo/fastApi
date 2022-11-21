from fastapi import APIRouter, Request, Depends
from modules.CRUD import SQL
from modules.TOOLS import parse_params_to_sql, payload_
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/{table}", tags=["API"], summary="內部取得資料", description="供內部使用可分為依參數取得部分資料或一次取得所有資料")
async def get_data(request: Request, table: str) -> tuple:
    if not request.query_params:
        json_compatible_item_data = jsonable_encoder(await SQL.get(request.app.state.pool, table))
        return JSONResponse(content=json_compatible_item_data)

    else:
        res = await SQL.query(request.app.state.pool,
                              table, f"SELECT * FROM {table} WHERE {parse_params_to_sql(request.query_params)}")
        json_compatible_item_data = jsonable_encoder(res)
        return JSONResponse(content=json_compatible_item_data)


@router.post("/{table}", tags=["API"], summary="新增、更新資料", description="可同時APPEND&UPDATE")
async def post_data(request: Request, table: str, payload: dict = Depends(payload_)):
    await SQL.update(request.app.state.pool, table, payload)
    return "1|OK"
