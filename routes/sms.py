from fastapi import APIRouter, BackgroundTasks, Request, Path
from modules.SMS import SMS

router = APIRouter()


@router.post("/{receiver}", tags=['SMS'])
async def send_email(receiver: str, request: Request, background_tasks: BackgroundTasks):
    payload = dict(await request.form())
    try:
        payload.update(await request.json())
    except Exception as e:
        pass
    background_tasks.add_task(SMS.send, receiver, detail=payload['detail'])
    return '1|OK'

