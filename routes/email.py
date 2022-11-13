from fastapi import APIRouter, BackgroundTasks, Request
from modules.EMAIL import EMAIL
router = APIRouter()


@router.post("/{receiver}", tags=['EMAIL'])
async def send_email(receiver: str, request: Request, background_tasks: BackgroundTasks):
    payload = dict(await request.form())
    try:
        payload.update(await request.json())
    except Exception as e:
        pass
    background_tasks.add_task(EMAIL.send, receiver, subject=payload['subject'], detail=payload['detail'])
    return '1|OK'

