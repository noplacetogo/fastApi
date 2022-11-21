from fastapi import APIRouter, Depends, Request, HTTPException
from routes import api, upload, line, \
    payment, email, sms, logistic, \
    member
from modules.TOOLS import parse_params_to_sql
import json
router = APIRouter()


# api紀錄操作使用
async def api_record(request: Request, user: dict = Depends(member.get_current_active_user)):
    content = ""
    if request.path_params :
        content = parse_params_to_sql(request.query_params)
    else:
        _payload = {}
        try:
            _payload = dict(await request.form())
            _payload.update(await request.json())
        except Exception as e:
            pass
        content = json.dumps(_payload)

    # api 紀錄操縱人
    record = {
        "username": user.username,
        "ip": request.client.host,
        "path": request.url.path,
        "method": request.method,
        "payload":  content
    }
    print(record)


# api權限確認
async def routes_permission_check(request: Request, user: dict = Depends(member.get_current_active_user)):
    #  有無帶參  帶參單一查詢、 不帶參多重查詢
    if not request.query_params:
        if request.url.path[1:].replace('/', ':') + ":" + request.method + ':ALL' not in user.scope:
            raise HTTPException(status_code=401, detail="No permission")
    else:
        if request.url.path[1:].replace('/', ':') + ":" + request.method not in user.scope:
            raise HTTPException(status_code=401, detail="No permission")

# a
router.include_router(
    api.router,
    prefix="/api",
    dependencies=[Depends(api_record), Depends(routes_permission_check)]
)

router.include_router(
    upload.router,
    prefix="/upload"
)

router.include_router(
    line.router,
    prefix="/line"
)

router.include_router(
    email.router,
    prefix="/email"
)

router.include_router(
    sms.router,
    prefix="/sms"
)

router.include_router(
    logistic.router,
    prefix="/logistic"
)

router.include_router(
    payment.router,
    prefix="/payment"
)

router.include_router(
    member.router,
    prefix="/member"
)